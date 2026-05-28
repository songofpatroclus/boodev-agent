import os 
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_dir,"r") as f:
            file_content_string = f.read(MAX_CHARS)
            
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File {file_path} truncated: True. at {MAX_CHARS} characters]'
        
        return file_content_string
        
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    # Moved the detailed explanation up to the main function description:
    description="Reads the content of a specified file within the permitted working directory and returns up to MAX_CHARS characters. If the file exceeds MAX_CHARS, it truncates the output.", 
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                # Simplified the parameter description to just explain the variable:
                description="The exact name or relative path of the file to read (e.g., 'main.py' or 'pkg/data.txt').", 
            ),
        },
        required=["file_path"]
    ),
)
