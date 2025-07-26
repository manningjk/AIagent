import os

def get_files_info(working_directory, directory="."):
    try:
        # Resolve paths safely
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory = os.path.abspath(working_directory)

        # Security check: prevent path traversal outside working_directory
        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            return f'Error: Directory "{directory}" does not exist.'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory.'

        entries = os.listdir(full_path)
        if not entries:
            return f'The directory "{directory}" is empty.'

        result_lines = []
        for entry in sorted(entries):
            entry_path = os.path.join(full_path, entry)
            is_dir = os.path.isdir(entry_path)
            size = os.path.getsize(entry_path) if not is_dir else 128  # default size for dirs
            result_lines.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"
