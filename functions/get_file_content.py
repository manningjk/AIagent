import os
from .config import MAX_FILE_CHARACTERS

def get_file_content(working_directory, file_path):
    try:
        # Resolve full absolute paths
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Prevent access outside the working directory
        if not full_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if file exists and is a regular file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file contents
        with open(full_path, 'r', encoding='utf-8') as f:
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

