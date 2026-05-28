import os
from config import MAX_CHARS
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        
        if not valid_target_dir:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        
        if valid_target_dir:
            parent_dir = os.path.dirname(target_dir)
            os.makedirs(parent_dir, exist_ok=True)  

        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    # Moved the detailed explanation up to the main function description:
    description="Writes content to a specified file path within the permitted working directory, creating any necessary directories.", 
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                # Simplified the parameter description to just explain the variable:
                description="The exact name or relative path of the file to write (e.g., 'main.py' or 'pkg/data.txt').", 
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file "
            )

        },
        required=["file_path","content"]
    ),
)
