import os
from google.genai import types
from .config import MAX_FILE_CHARACTERS

def get_file_content(working_directory, file_path):
    try:
        # Resolve full absolute paths
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Prevent access outside the working directory
        if not file_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if file exists and is a regular file
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file contents
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # Truncate if too long
        if len(content) > MAX_FILE_CHARACTERS:
            trunc_content = content[:MAX_FILE_CHARACTERS] + f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARACTERS} characters]'
            return trunc_content
        
        # Return full content if within limits
        else:
            return content

    except Exception as e:
        return f"Error: {str(e)}"

# Schema definition for the get_file_content function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file content in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to read files from, relative to the working directory. If not provided, reads files in the working directory itself.",
            ),
        },
    ),
)
