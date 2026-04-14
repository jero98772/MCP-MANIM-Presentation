"""
server.py — Minimal MCP server over raw TCP sockets
Protocol: JSON-RPC 2.0 (newline-delimited)

Supports:
  initialize    → server handshake + capabilities
  tools/list    → returns available tools schema
  tools/call    → executes a tool and returns result
"""

import socket
import json
import math

HOST = "127.0.0.1"
PORT = 9000


# ── Tool registry ────────────────────────────────────────────────────────────


def calculate(expression: str) -> str:
    safe_builtins = {"__builtins__": {}, "abs": abs, "round": round, "math": math}
    try:
        result = eval(expression, safe_builtins)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def get_weather(city: str, unit: str = "celsius") -> dict:
    mock = {
        "london": {"temp": 14, "condition": "Cloudy"},
        "new york": {"temp": 22, "condition": "Sunny"},
        "tokyo": {"temp": 28, "condition": "Humid"},
        "medellin": {"temp": 22, "condition": "Partly Cloudy"},
    }
    data = mock.get(city.lower())
    if not data:
        return {"error": f"No data for '{city}'"}
    if unit == "fahrenheit":
        data = dict(data)
        data["temp"] = round(data["temp"] * 9 / 5 + 32, 1)
    return {**data, "city": city, "unit": unit}


TOOLS = {
    "calculate": {
        "fn": calculate,
        "schema": {
            "name": "calculate",
            "description": "Evaluates a math expression and returns the result.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "e.g. '(12 + 8) * 3'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    "get_weather": {
        "fn": get_weather,
        "schema": {
            "name": "get_weather",
            "description": "Returns current weather conditions for a given city.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["city"],
            },
        },
    },
}


# ── JSON-RPC helpers ──────────────────────────────────────────────────────────


def ok(id_, result):
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def err(id_, code, message):
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


# ── Request dispatcher ────────────────────────────────────────────────────────


def handle(request: dict) -> dict:
    method = request.get("method")
    id_ = request.get("id")
    params = request.get("params", {})

    print(f"  ← [{method}] id={id_}")

    if method == "initialize":
        return ok(
            id_,
            {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "minimal-mcp-server", "version": "1.0.0"},
                "capabilities": {"tools": {}},
            },
        )

    if method == "tools/list":
        return ok(id_, {"tools": [t["schema"] for t in TOOLS.values()]})

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})

        if name not in TOOLS:
            return err(id_, -32601, f"Unknown tool: '{name}'")

        try:
            result = TOOLS[name]["fn"](**arguments)
            return ok(id_, {"content": [{"type": "text", "text": json.dumps(result)}]})
        except Exception as e:
            return err(id_, -32603, str(e))

    return err(id_, -32601, f"Method not found: '{method}'")


# ── Server loop ───────────────────────────────────────────────────────────────


def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"MCP server listening on {HOST}:{PORT}\n")

        while True:
            conn, addr = server.accept()
            print(f"Client connected: {addr}")
            with conn:
                buf = ""
                while True:
                    chunk = conn.recv(4096).decode()
                    if not chunk:
                        break
                    buf += chunk
                    # Messages are newline-delimited JSON
                    while "\n" in buf:
                        line, buf = buf.split("\n", 1)
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            request = json.loads(line)
                            response = handle(request)
                            payload = json.dumps(response) + "\n"
                            conn.sendall(payload.encode())
                            print(f"  → sent response for id={response.get('id')}\n")
                        except json.JSONDecodeError as e:
                            resp = err(None, -32700, f"Parse error: {e}")
                            conn.sendall((json.dumps(resp) + "\n").encode())
            print("Client disconnected.\n")


if __name__ == "__main__":
    serve()
