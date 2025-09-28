def run_python_file(working_directory, file_path, args=[]):
    import os
    import subprocess
    import sys
    
    # Create absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    # Security check: ensure file is within working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check if file exists
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    # Check if file is a Python file
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # Prepare the command
        python_executable = sys.executable
        command = [python_executable, abs_file_path] + args
        
        # Run the command and capture output
        completed_process = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Prepare the output
        output = []
        
        # Check if there's any stdout
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        
        # Check if there's any stderr
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")
        
        # Check if process exited with non-zero code
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        
        # If no output was produced
        if not output:
            return "No output produced."
        
        # Join all parts of the output
        return '\n'.join(output)
        
    except subprocess.TimeoutExpired:
        return "Error: execution timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"