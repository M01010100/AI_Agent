def write_file(working_directory, file_path, content):
    import os
    
    # Create absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    # Security check: ensure file is within working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        
        # Write content to the file
        with open(abs_file_path, 'w') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {str(e)}"