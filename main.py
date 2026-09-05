import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("API key not set")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        final_response = message.content or ""
        print(final_response.encode("ascii", errors="replace").decode("ascii"))
        break

    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, args.verbose)
        if not result_message["content"]:
            raise RuntimeError("Function returned empty content")
        if args.verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)
else:
    print("Error: Agent reached maximum iterations without producing a final response.")
    raise SystemExit(1)