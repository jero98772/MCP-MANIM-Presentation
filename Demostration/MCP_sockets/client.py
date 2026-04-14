"""
client.py — MCP client + OpenAI agent
Flow:
  1. Connect to MCP server via TCP socket
  2. initialize  → handshake
  3. tools/list  → discover tools, convert to OpenAI schema
  4. run_agent() → LLM decides which tools to call → client executes via MCP socket
"""

import socket
import json
from openai import OpenAI

HOST = "127.0.0.1"
PORT = 9000

# ── Transport ─────────────────────────────────────────────────────────────────


class MCPClient:
    def __init__(self):
        self._sock = None
        self._buf = ""
        self._req_id = 0

    def connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((HOST, PORT))
        print(f"[MCP] Connected to {HOST}:{PORT}")

    def close(self):
        if self._sock:
            self._sock.close()

    def _next_id(self) -> int:
        self._req_id += 1
        return self._req_id

    def _send(self, method: str, params: dict = None) -> dict:
        payload = {"jsonrpc": "2.0", "id": self._next_id(), "method": method}
        if params:
            payload["params"] = params
        self._sock.sendall((json.dumps(payload) + "\n").encode())

        while "\n" not in self._buf:
            chunk = self._sock.recv(4096).decode()
            if not chunk:
                raise ConnectionError("Server closed the connection.")
            self._buf += chunk

        line, self._buf = self._buf.split("\n", 1)
        return json.loads(line.strip())

    # ── MCP protocol ──────────────────────────────────────────────────────────

    def initialize(self):
        resp = self._send(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "clientInfo": {"name": "mcp-openai-client", "version": "1.0.0"},
                "capabilities": {},
            },
        )
        info = resp.get("result", {}).get("serverInfo", {})
        print(f"[MCP] Server: {info.get('name')} v{info.get('version')}")

    def list_tools(self) -> list[dict]:
        resp = self._send("tools/list")
        return resp.get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: dict) -> str:
        resp = self._send("tools/call", {"name": name, "arguments": arguments})
        if "error" in resp:
            return f"Error: {resp['error']['message']}"
        content = resp.get("result", {}).get("content", [])
        return content[0]["text"] if content else "(empty result)"


# ── Schema conversion: MCP → OpenAI ──────────────────────────────────────────


def mcp_tools_to_openai(mcp_tools: list[dict]) -> list[dict]:
    """
    MCP schema uses 'inputSchema'.
    OpenAI function-calling uses 'parameters'.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["inputSchema"],
            },
        }
        for t in mcp_tools
    ]


# ── Agent loop ────────────────────────────────────────────────────────────────


def run_agent(
    user_input: str,
    mcp: MCPClient,
    openai_tools: list[dict],
    llm: OpenAI,
    model: str = "gpt-4o",
):
    messages = [{"role": "user", "content": user_input}]

    print(f"\n{'='*60}")
    print(f"USER: {user_input}")
    print(f"{'='*60}")

    for iteration in range(10):
        response = llm.chat.completions.create(
            model=model,
            messages=messages,
            tools=openai_tools,
            tool_choice="auto",
            temperature=0,
        )

        msg = response.choices[0].message
        messages.append(msg)

        # No tool calls → LLM has a final answer
        if not msg.tool_calls:
            print(f"\nASSISTANT: {msg.content}")
            return msg.content

        # LLM wants to call one or more tools
        for tc in msg.tool_calls:
            tool_name = tc.function.name
            arguments = json.loads(tc.function.arguments)

            print(f"\n[iter {iteration+1}] LLM → tools/call: {tool_name}")
            print(f"  args  : {json.dumps(arguments)}")

            # Execute via MCP socket (not locally!)
            result = mcp.call_tool(tool_name, arguments)

            print(f"  result: {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                }
            )

    return "Max iterations reached."


# ── Main ──────────────────────────────────────────────────────────────────────


def main():
    llm = OpenAI(
        api_key="YOUR_API_KEY_HERE",
        base_url="http://localhost:1234/v1",
    )

    mcp = MCPClient()
    mcp.connect()

    # ── 1. Handshake ──────────────────────────────────────────────────────────
    mcp.initialize()

    # ── 2. Discover tools and convert schema ──────────────────────────────────
    mcp_tools = mcp.list_tools()
    openai_tools = mcp_tools_to_openai(mcp_tools)

    print(f"[MCP] {len(mcp_tools)} tools available: {[t['name'] for t in mcp_tools]}\n")

    # ── 3. Run queries — the LLM drives everything ────────────────────────────
    queries = [
        "What is (144 / 12) + 7 * 3?",
        "What's the weather like in Tokyo in Fahrenheit?",
        "What is 2 + 2? Also, what's the weather in London?",
    ]

    for query in queries:
        run_agent(query, mcp, openai_tools, llm)
        print()

    mcp.close()


if __name__ == "__main__":
    main()
