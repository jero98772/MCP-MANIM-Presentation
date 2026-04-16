import json
import inspect
from pathlib import Path
from openai import OpenAI

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


def serialize_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"],
            },
        }
        for t in _registry.values()
    ]


def calculate(expression):
    print("The code is calling Calculate File")
    return eval(expression, {"__builtins__": {}})


def get_weather(city, unit="celsius"):
    mock_data = {
        "london": {"temp": 14, "condition": "Cloudy", "humidity": 72},
        "new york": {"temp": 22, "condition": "Sunny", "humidity": 55},
        "tokyo": {"temp": 28, "condition": "Humid", "humidity": 80},
        "paris": {"temp": 17, "condition": "Rainy", "humidity": 68},
        "sydney": {"temp": 24, "condition": "Clear", "humidity": 50},
        "medellin": {"temp": 22, "condition": "Partly Cloudy", "humidity": 65},
    }
    key = city.lower()
    if key not in mock_data:
        return f"No weather data for '{city}'"
    data = dict(mock_data[key])
    if unit == "fahrenheit":
        data["temp"] = round(data["temp"] * 9 / 5 + 32, 1)
    data["unit"] = unit
    data["city"] = city
    return data


def convert_units(value, from_unit, to_unit):
    conversions = {
        ("km", "miles"): lambda x: round(x * 0.621371, 4),
        ("miles", "km"): lambda x: round(x * 1.60934, 4),
        ("kg", "lbs"): lambda x: round(x * 2.20462, 4),
        ("lbs", "kg"): lambda x: round(x * 0.453592, 4),
        ("c", "f"): lambda x: round(x * 9 / 5 + 32, 2),
        ("f", "c"): lambda x: round((x - 32) * 5 / 9, 2),
        ("meters", "feet"): lambda x: round(x * 3.28084, 4),
        ("feet", "meters"): lambda x: round(x * 0.3048, 4),
    }
    key = (from_unit.lower(), to_unit.lower())
    if key not in conversions:
        return f"Conversion from '{from_unit}' to '{to_unit}' not supported"
    return conversions[key](value)


def search_knowledge_base(query):
    kb = {
        "python": "Python is a high-level, interpreted programming language known for its readability and versatility.",
        "openai": "OpenAI is an AI research company that develops models like GPT-4 and offers APIs for AI-powered applications.",
        "llm": "Large Language Models (LLMs) are deep learning models trained on massive text corpora to understand and generate human language.",
        "tool calling": "Tool calling allows LLMs to invoke external functions, APIs, or tools to augment their capabilities.",
        "api": "An API (Application Programming Interface) defines how software components communicate with each other.",
    }
    matches = {k: v for k, v in kb.items() if query.lower() in k}
    return matches if matches else f"No entry found for '{query}'"


def write_file(filename, content):
    print("The code is calling write File")
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"Written {len(content.encode('utf-8'))} bytes to '{filename}'"


register_tool(
    calculate,
    name="calculate",
    description="Evaluates a mathematical expression and returns the numeric result.",
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Math expression, e.g. '(12 + 8) * 3'",
            }
        },
        "required": ["expression"],
    },
)

register_tool(
    get_weather,
    name="get_weather",
    description="Returns current weather conditions for a given city.",
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name, e.g. 'Tokyo'"},
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit.",
            },
        },
        "required": ["city"],
    },
)

register_tool(
    convert_units,
    name="convert_units",
    description="Converts a value between units. Supported: km-miles, kg-lbs, C-F, meters-feet.",
    parameters={
        "type": "object",
        "properties": {
            "value": {"type": "number", "description": "Value to convert."},
            "from_unit": {"type": "string", "description": "Unit to convert from."},
            "to_unit": {"type": "string", "description": "Unit to convert to."},
        },
        "required": ["value", "from_unit", "to_unit"],
    },
)

register_tool(
    search_knowledge_base,
    name="search_knowledge_base",
    description="Searches an internal knowledge base for technical terms and concepts.",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Term to search for."}
        },
        "required": ["query"],
    },
)

register_tool(
    write_file,
    name="write_file",
    description="Writes text content to a file, creating it and any missing directories if needed.",
    parameters={
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "File path, e.g. 'output.txt' or 'notes/summary.md'.",
            },
            "content": {"type": "string", "description": "Text content to write."},
        },
        "required": ["filename", "content"],
    },
)


def execute_tool(tool_name, arguments):
    tool_entry = get_tool(tool_name)
    fn = tool_entry["fn"]
    sig = inspect.signature(fn)
    bound = sig.bind(**arguments)
    bound.apply_defaults()
    return fn(*bound.args, **bound.kwargs)


def run_agent(user_input, client, model="gpt-4o", max_iterations=10):
    messages = [{"role": "user", "content": user_input}]

    print(f"\n{'='*60}\nUSER: {user_input}\n{'='*60}")

    for iteration in range(max_iterations):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=serialize_tools(),
            tool_choice="auto",
            temperature=0,
        )

        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            print(f"\nASSISTANT: {msg.content}")
            return msg.content

        for tc in msg.tool_calls:
            tool_name = tc.function.name
            arguments = json.loads(tc.function.arguments)

            print(f"\n[Iteration {iteration + 1}] Tool Call: {tool_name}")
            print(f"  -> Arguments: {json.dumps(arguments, indent=4)}")

            result = execute_tool(tool_name, arguments)

            print(f"  <- Result   : {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result),
                }
            )

    return "Max iterations reached without a final answer."


if __name__ == "__main__":
    client = OpenAI(
        api_key="YOUR_API_KEY_HERE",
        base_url="http://localhost:1234/v1",
    )

    demo_queries = [
        'Write "Hello, World!" to a file called hello.txt.',
        "What is (144 / 12) + 7 * 3?",
        "What's the weather like in Medellin in Fahrenheit?",
        "Convert 100 km to miles.",
        "Can you explain what an LLM is?",
        "What is 2 + 2? Also, what's the weather in Medellin?",
    ]

    for query in demo_queries:
        run_agent(query, client)
        print()
