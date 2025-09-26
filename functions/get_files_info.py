def get_files_info(working_directory, directory="."):
    import os

       # Create absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    target_directory = os.path.abspath(os.path.join(abs_working_dir, directory))
    
    # Security check: ensure target is within working directory
    if not target_directory.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Check if target is actually a directory
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'
    
    try:
        result = []
        # List all items in the directory
        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)
            is_dir = os.path.isdir(item_path)
            size = 0
            
            if is_dir:
                # Calculate directory size
                for dirpath, dirnames, filenames in os.walk(item_path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.isfile(fp):
                            size += os.path.getsize(fp)
            else:
                # Get file size
                size = os.path.getsize(item_path)
                
            result.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        
        return '\n'.join(result) if result else "Directory is empty"
        
    except Exception as e:
        return f"Error: {str(e)}"
    

    