import os
import sys

# Add the project root directory to the Python path to make imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import MAX_FILE_SIZE_CHARS

def get_file_content(working_directory, file_path):
    
    # Create absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    # Security check: ensure file is within working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if path is a regular file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        # Read file content
        with open(abs_file_path, 'r') as file:
            content = file.read()
        
        # Check if content needs truncation
        if len(content) > MAX_FILE_SIZE_CHARS:
            content = content[:MAX_FILE_SIZE_CHARS] + f"\n[...File \"{file_path}\" truncated at {MAX_FILE_SIZE_CHARS} characters]"
        
        return content
        
    except Exception as e:
        return f"Error: {str(e)}"