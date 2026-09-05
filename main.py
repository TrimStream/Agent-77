import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt

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

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ],
)

if args.verbose:
    if response.usage is None:
        raise RuntimeError(
            "Response usage is None. This may indicate a failed API request."
        )
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")

print(response.choices[0].message.content)