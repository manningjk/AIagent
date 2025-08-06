import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


# Load environment
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# System instruction
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Handle CLI arguments
args = sys.argv[1:]
if not args:
    print("Error: No prompt provided!")
    sys.exit(1)

verbose = False
if "--verbose" in args:
    verbose = True
    args.remove("--verbose")

user_prompt = " ".join(args)

# Message history: system + user
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Register tools
available_functions = types.Tool(function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
])

config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
)

# Main reasoning loop
max_iterations = 20
for i in range(max_iterations):
    if verbose:
        print(f"\n--- Iteration {i + 1} ---")

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=config
        )
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)

    if not response.candidates:
        print("No candidates returned from Gemini.")
        break

    candidate = response.candidates[0]
    content = candidate.content
    messages.append(content)

    function_called = False
    final_response = False

    for part in content.parts:
        # Handle function calls
        if hasattr(part, "function_call") and part.function_call:
            fn_call = part.function_call
            if not fn_call.name:
                print("Function call name missing.")
                continue

            if verbose:
                print(f"Calling function: {fn_call.name}")
                print(f"Arguments: {fn_call.args}")

            function_result = call_function(fn_call, verbose=verbose)
            messages.append(function_result)

            if verbose and function_result.parts:
                response_part = function_result.parts[0]
                if hasattr(response_part, "function_response"):
                    print("-> Function response:", response_part.function_response.response)

            function_called = True

        # Handle final text response
        elif hasattr(part, "text") and part.text.strip():
            final_response = True
            print("\nAI Response:\n" + part.text)

    if final_response and not function_called:
        break  # We're done — the agent gave its final answer
