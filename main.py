import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


# Load environment variables
load_dotenv()

# Fetch the API key
api_key = os.environ.get("GEMINI_API_KEY")
# Initialize the Gemini client
client = genai.Client(api_key=api_key)


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


# Handle input arguments
if len(sys.argv) < 2:
    print("Error: No prompt provided!")
    sys.exit(1)

user_prompt = sys.argv[1]
verbose = False
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    verbose = True

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]), 
]

# Register tools with functions declarations
available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file])

config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages, 
    config=config
)

if response.function_calls:
    function_call_part = response.function_calls[0]
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(response.text)
if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

