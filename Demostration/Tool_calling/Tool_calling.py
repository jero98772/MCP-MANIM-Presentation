import os
import json
import inspect
import re
from openai import OpenAI

# ─────────────────────────────────────────────
# TOOL REGISTRY
# ─────────────────────────────────────────────

_registry = {}

def register_tool(fn, name, description, parameters):
    _registry[name] = {
        "fn": fn,
        "name": name,
        "description": description,
        "parameters": parameters,
    }

def get_tool(name):
    return _registry.get(name)

def all_tools():
    return list(_registry.values())

def serialize_tools():
    return [
        {
            "name": t["name"],
            "description": t["description"],
            "parameters": t["parameters"],
        }
        for t in all_tools()
    ]


# ─────────────────────────────────────────────
# TOOL DEFINITIONS (plain Python functions)
# ─────────────────────────────────────────────

def calculate(expression):
    print("calculated bro")
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return {"error": f"Invalid characters in expression: {expression}"}
    result = eval(expression)
    return {"result": result}

def get_weather(city, unit="celsius"):
    mock_data = {
        "london":    {"temp": 14, "condition": "Cloudy",  "humidity": 72},
        "new york":  {"temp": 22, "condition": "Sunny",   "humidity": 55},
        "tokyo":     {"temp": 28, "condition": "Humid",   "humidity": 80},
        "paris":     {"temp": 17, "condition": "Rainy",   "humidity": 68},
        "sydney":    {"temp": 24, "condition": "Clear",   "humidity": 50},
        "medellin":  {"temp": 22, "condition": "Partly Cloudy", "humidity": 65},
    }
    key = city.lower()
    if key not in mock_data:
        return {"error": f"No weather data available for '{city}'"}
    data = dict(mock_data[key])
    if unit == "fahrenheit":
        data["temp"] = round(data["temp"] * 9 / 5 + 32, 1)
    data["unit"] = unit
    data["city"] = city
    return data

def convert_units(value, from_unit, to_unit):
    conversions = {
        ("km", "miles"):    lambda x: round(x * 0.621371, 4),
        ("miles", "km"):    lambda x: round(x * 1.60934,  4),
        ("kg", "lbs"):      lambda x: round(x * 2.20462,  4),
        ("lbs", "kg"):      lambda x: round(x * 0.453592, 4),
        ("c", "f"):         lambda x: round(x * 9 / 5 + 32, 2),
        ("f", "c"):         lambda x: round((x - 32) * 5 / 9, 2),
        ("meters", "feet"): lambda x: round(x * 3.28084,  4),
        ("feet", "meters"): lambda x: round(x * 0.3048,   4),
    }
    key = (from_unit.lower(), to_unit.lower())
    if key not in conversions:
        return {"error": f"Conversion from '{from_unit}' to '{to_unit}' is not supported"}
    converted = conversions[key](value)
    return {"original": value, "from": from_unit, "to": to_unit, "result": converted}

def search_knowledge_base(query):
    kb = {
        "python":      "Python is a high-level, interpreted programming language known for its readability and versatility.",
        "openai":      "OpenAI is an AI research company that develops models like GPT-4 and offers APIs for AI-powered applications.",
        "llm":         "Large Language Models (LLMs) are deep learning models trained on massive text corpora to understand and generate human language.",
        "tool calling":"Tool calling (function calling) allows LLMs to invoke external functions, APIs, or tools to augment their capabilities.",
        "api":         "An API (Application Programming Interface) defines how software components communicate with each other.",
    }
    matches = {k: v for k, v in kb.items() if query.lower() in k}
    if not matches:
        return {"result": None, "message": f"No knowledge base entry found for '{query}'"}
    return {"results": matches}


register_tool(
    calculate,
    name="calculate",
    description="Evaluates a mathematical expression and returns the numeric result. Use for arithmetic, algebra, or any computation involving numbers.",
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "A valid mathematical expression using numbers and operators (+, -, *, /, parentheses). Example: '(12 + 8) * 3 / 4'"
            }
        },
        "required": ["expression"]
    }
)

register_tool(
    get_weather,
    name="get_weather",
    description="Returns current weather conditions for a given city. Supports major world cities. Temperatures can be returned in celsius or fahrenheit.",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city to get weather for, e.g., 'London', 'New York', 'Tokyo'"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit. Defaults to 'celsius'."
            }
        },
        "required": ["city"]
    }
)

register_tool(
    convert_units,
    name="convert_units",
    description="Converts a numeric value between units of measurement. Supported pairs: km↔miles, kg↔lbs, C↔F, meters↔feet.",
    parameters={
        "type": "object",
        "properties": {
            "value": {
                "type": "number",
                "description": "The numeric value to convert."
            },
            "from_unit": {
                "type": "string",
                "description": "The unit to convert from (e.g., 'km', 'kg', 'c', 'meters')."
            },
            "to_unit": {
                "type": "string",
                "description": "The unit to convert to (e.g., 'miles', 'lbs', 'f', 'feet')."
            }
        },
        "required": ["value", "from_unit", "to_unit"]
    }
)

register_tool(
    search_knowledge_base,
    name="search_knowledge_base",
    description="Searches an internal knowledge base for definitions or explanations of technical terms and concepts.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The keyword or topic to search for (e.g., 'python', 'llm', 'api')."
            }
        },
        "required": ["query"]
    }
)


# ─────────────────────────────────────────────
# PROMPT CONSTRUCTION
# ─────────────────────────────────────────────

TOOL_CALL_RULES = """
You are an intelligent assistant with access to external tools.

RULES:
1. Only call a tool if the user's request genuinely requires it.
2. When calling a tool, respond ONLY with a valid JSON object — nothing else. No prose, no explanation.
3. The JSON format for a tool call is exactly:
   {{"tool": "<tool_name>", "arguments": {{<key-value pairs>}}}}
4. Do NOT invent tool names or parameter names not listed below.
5. Do NOT call multiple tools at once. Call one at a time.
6. After receiving a tool result, use it to compose your final natural-language answer.
7. If the user's request is ambiguous, ask for clarification instead of guessing.
8. If no tool is needed, respond directly in natural language.

AVAILABLE TOOLS:
{tool_descriptions}
"""

def build_system_prompt():
    tool_descriptions = json.dumps(serialize_tools(), indent=2)
    return TOOL_CALL_RULES.format(tool_descriptions=tool_descriptions)


# ─────────────────────────────────────────────
# RESPONSE PARSER
# ─────────────────────────────────────────────

def extract_json_block(text):
    text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence_match:
        return fence_match.group(1)
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        return brace_match.group(0)
    return None

def parse_tool_call(response_text):
    raw = extract_json_block(response_text)
    if raw is None:
        return None
    parsed = json.loads(raw)
    if "tool" not in parsed or "arguments" not in parsed:
        return None
    return parsed

def validate_arguments(tool_entry, arguments):
    schema = tool_entry["parameters"]
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    missing = [r for r in required if r not in arguments]
    if missing:
        return False, f"Missing required arguments: {missing}"
    for key, val in arguments.items():
        if key not in properties:
            return False, f"Unknown argument: '{key}'"
    return True, None


# ─────────────────────────────────────────────
# EXECUTION ENGINE
# ─────────────────────────────────────────────

def execute_tool(tool_name, arguments):
    tool_entry = get_tool(tool_name)
    if tool_entry is None:
        return {"error": f"Tool '{tool_name}' is not registered."}
    valid, error_msg = validate_arguments(tool_entry, arguments)
    if not valid:
        return {"error": error_msg}
    fn = tool_entry["fn"]
    sig = inspect.signature(fn)
    bound = sig.bind(**arguments)
    bound.apply_defaults()
    result = fn(*bound.args, **bound.kwargs)
    return result


# ─────────────────────────────────────────────
# CONVERSATION LOOP
# ─────────────────────────────────────────────

def run_agent(user_input, client, model="gpt-4o", max_iterations=10):
    messages = [
        {"role": "system",  "content": build_system_prompt()},
        {"role": "user",    "content": user_input},
    ]

    print(f"\n{'═'*60}")
    print(f"USER: {user_input}")
    print(f"{'═'*60}")

    for iteration in range(max_iterations):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )

        assistant_message = response.choices[0].message
        content = assistant_message.content or ""
        messages.append({"role": "assistant", "content": content})

        tool_call = parse_tool_call(content)

        if tool_call is None:
            print(f"\nASSISTANT: {content}")
            return content

        tool_name = tool_call["tool"]
        arguments = tool_call["arguments"]

        print(f"\n[Iteration {iteration + 1}] Tool Call Detected")
        print(f"  → Tool     : {tool_name}")
        print(f"  → Arguments: {json.dumps(arguments, indent=4)}")

        tool_result = execute_tool(tool_name, arguments)
        result_str = json.dumps(tool_result)

        print(f"  ← Result   : {result_str}")

        messages.append({
            "role": "user",
            "content": f"Tool '{tool_name}' returned: {result_str}"
        })

    return "Max iterations reached without a final answer."


# ─────────────────────────────────────────────
# ENTRYPOINT / DEMO
# ─────────────────────────────────────────────

if __name__ == "__main__":
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE"),
        base_url=os.environ.get("OPENAI_BASE_URL", "http://localhost:1234/v1"),
    )

    demo_queries = [
        "What is (144 / 12) + 7 * 3?",
        "What's the weather like in Tokyo in Fahrenheit?",
        "Convert 100 km to miles.",
        "Can you explain what an LLM is?",
        "What is 2 + 2? Also, what's the weather in London?",
    ]

    for query in demo_queries:
        run_agent(query, client)
        print()
