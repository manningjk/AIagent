import os
from google.genai import types


# Function to get files information
def get_files_info(working_directory, directory="."):
    try:
        # Resolve paths safely
        file_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)

        # Security check: prevent access outside working_directory
        if not file_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.exists(file_path):
            return f'Error: Directory "{directory}" does not exist.'

        if not os.path.isdir(file_path):
            return f'Error: "{directory}" is not a directory.'

        entries = os.listdir(file_path)
        if not entries:
            return f'The directory "{directory}" is empty.'

        result_lines = []
        for entry in sorted(entries):
            entry_path = os.path.join(file_path, entry)
            is_dir = os.path.isdir(entry_path)
            size = os.path.getsize(entry_path) if not is_dir else 128  # default size for dirs
            result_lines.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"

# Schema definition for the get_files_info function
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
