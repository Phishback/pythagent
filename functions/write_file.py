import os
from google.genai import types

def write_file(working_dir, file_path, content):
    absolute_dir_path = os.path.abspath(working_dir)
    target_file_path = os.path.normpath(os.path.join(absolute_dir_path,file_path))
    valid_file_path = os.path.commonpath([absolute_dir_path, target_file_path]) == absolute_dir_path

    if valid_file_path == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    try:
        parent_dir = os.path.dirname(target_file_path)
        os.makedirs(parent_dir, exist_ok=True)
        with open(target_file_path, "w") as open_file_path:
            open_file_path.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except (PermissionError, OSError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content to the file from specified directory relative to the working directory and given file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
                "working_dir": types.Schema(
                    type=types.Type.STRING,
                    description="Working directory path or Directory to write the content of file, relative to the working directory.",
                ),
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="File path to the file to write the contents too"
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="Content to be written in given file from file_path"
                )
        },
    ),
)
