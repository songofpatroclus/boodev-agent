import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        # Use abspath here to ensure we have the full path for the file too
        target_path_abs = os.path.abspath(os.path.join(working_directory, file_path))
        
        # Step 2: Validation
        if os.path.commonpath([working_dir_abs, target_path_abs]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Step 3 & 4: File checks
        if not os.path.isfile(target_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        # Step 5 & 6: Build command
        command = ["python", target_path_abs]
        if args:
            command.extend(args)

        # Step 7: Run process
        res = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Step 8: Build output string
        output = ""
        if res.returncode != 0:
            output += f"Process exited with code {res.returncode}\n"
        
        if not res.stdout and not res.stderr:
            output += "No output produced"
        else:
            if res.stdout:
                output += f"STDOUT: {res.stdout}" # Note the space after colon per standard formatting
            if res.stderr:
                output += f"STDERR: {res.stderr}"

        return output.strip()

    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python script from the specified directory, providing detailed output including stdout and stderr.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The exact path of the Python file to run (e.g., 'main.py').", # Fixed description
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="An optional list of command-line arguments to pass to the Python script.",
            ),
        },
        required=["file_path"] # 'args' is left out of required since it's optional
    ),
)