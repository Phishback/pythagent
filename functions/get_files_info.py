import os
from google.genai import types


def get_files_info(working_dir, dir="."):
    try:
        absolute_dir_path = os.path.abspath(working_dir)
        target_dir = os.path.normpath(os.path.join(absolute_dir_path, dir))
        valid_target_dir = os.path.commonpath(
            [absolute_dir_path, target_dir]) == absolute_dir_path

        if valid_target_dir == False:
            return f'Error: Cannot list "{dir}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) != True:
            return f'Error: "{dir}" is not a directory'

        results = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            results.append(
                f"- {item}: file_size={os.path.getsize(item_path)}bytes, is_dir={os.path.isdir(item_path)}")
        return "\n".join(results)
    except Exception as e:
        return f"Error:{e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
                "working_dir": types.Schema(
                    type=types.Type.STRING,
                    description="Working directory path, relative to the root (e.g., './calculator')",
                ),
                "dir": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself",
                ),
        },
    ),
)
