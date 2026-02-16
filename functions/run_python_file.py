import subprocess, os
from google.genai import types

def run_python_file(working_dir, file_path, args=None):
    absolute_dir_path = os.path.abspath(working_dir)
    target_file_path = os.path.normpath(os.path.join(absolute_dir_path,file_path))
    valid_file_path = os.path.commonpath([absolute_dir_path, target_file_path]) == absolute_dir_path

    if valid_file_path == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(target_file_path) == False:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if target_file_path.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = ['python', target_file_path]
        if args != None:
            command.extend(args)

        completed_process = subprocess.run(
                command,
                cwd=absolute_dir_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
        )
        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}"
        if completed_process.stdout == "" and completed_process.stderr == "":
            return "No output produced"

        completed_process_output = ""
        if completed_process.stdout:
            completed_process_output += f"STDOUT: {completed_process.stdout}"
        if completed_process.stderr:
            completed_process_output += f"STDERR: {completed_process.stderr}"
        return completed_process_output
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file relative to the working directory, provided file_path, and include arguments, from args, default is None",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
                "working_dir": types.Schema(
                    type=types.Type.STRING,
                    description="Working directory path or Directory to run Python file from, relative to the working directory.",
                ),
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Name of the Python file to run"
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    description="Array of optional arguments to pass to the python file to run. Contains items of type string",
                    items=types.Schema(
                        type=types.Type.STRING,
                        description="The optional arguments to be passed into the Python file being ran"
                    ),
                ),
        },
    ),
)
