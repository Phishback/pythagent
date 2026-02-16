import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_dir, file_path):
    absolute_dir_path = os.path.abspath(working_dir)
    target_file_path = os.path.normpath(os.path.join(absolute_dir_path,file_path))
    valid_file_path = os.path.commonpath([absolute_dir_path, target_file_path]) == absolute_dir_path

    if valid_file_path == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file_path) as open_file_path:
            content = open_file_path.read(MAX_CHARS)
            if open_file_path.read(1):
                content += f'\n[..File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except (FileNotFoundError, PermissionError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content files in a specified directory relative to the working directory and given file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
                "working_dir": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path or Directory to read content of file(s) from, relative to the working directory.",
                ),
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="File path to read the contents of or file to read its content"
                )
        },
    ),
)
