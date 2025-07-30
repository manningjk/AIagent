import os
import subprocess
from google.genai import types

# Schema definition for the run_python_file function
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to run python files from, relative to the working directory. If not provided, reads files in the working directory itself.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Resolve paths safely
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))
        relative_path = os.path.relpath(file_path, working_directory)
        file_name_only = os.path.basename(file_path)

        stdout_output = ""
        stderr_output = ""

        # Security check: prevent access outside working_directory
        if not file_path.startswith(working_directory):
            return f'Error: Cannot execute "{relative_path}" as it is outside the permitted working directory'
        
        # Check if the file exists
        elif not os.path.isfile(file_path):
            return f'Error: File "{file_name_only}" not found.'
        
        # Check if the file is a Python file
        elif not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        else:
            # Prepare the command to run the Python file
            command = ['python', file_path] + args

            # Execute the command and capture output
            results = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30, cwd=working_directory)

            stdout_output = results.stdout.strip()
            stderr_output = results.stderr.strip()

            if results.returncode != 0:
                stderr_output += f"\nProcess exited with code {results.returncode}"
        
        # Prepare the output
        output_parts = []
        if stdout_output:
            output_parts.append("STDOUT:\n" + stdout_output)
        if stderr_output:
            output_parts.append("STDERR:\n" + stderr_output)
        if not output_parts:
            output_parts.append("STDOUT:\nNo output produced.")
        
        return "\n".join(output_parts)

    except Exception as e:
        return f"STDOUT:\nError: executing python file: {e}"