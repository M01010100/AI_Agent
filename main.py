import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def setup_test_environment():
    """Create necessary files for testing if they don't exist."""
    # Ensure calculator directory exists
    os.makedirs("calculator/pkg", exist_ok=True)
    
    # Write a test file with 9 tests
    test_content = """
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)
    
    def test_subtract(self):
        self.assertEqual(5 - 3, 2)
    
    def test_multiply(self):
        self.assertEqual(2 * 3, 6)
    
    def test_divide(self):
        self.assertEqual(6 / 3, 2)
    
    def test_modulo(self):
        self.assertEqual(7 % 3, 1)
    
    def test_power(self):
        self.assertEqual(2 ** 3, 8)
    
    def test_floor_division(self):
        self.assertEqual(7 // 3, 2)
    
    def test_negative(self):
        self.assertEqual(-1 * 3, -3)
    
    def test_zero(self):
        self.assertEqual(0 * 5, 0)

if __name__ == '__main__':
    unittest.main()
"""
    write_file("./calculator", "tests.py", test_content)
    
    # Create lorem.txt
    lorem_content = "wait, this isn't lorem ipsum"
    write_file("./calculator", "lorem.txt", lorem_content)
    
    # Create simple README.md if it doesn't exist
    if not os.path.exists("./calculator/README.md"):
        write_file("./calculator", "README.md", "# Calculator\n\nA simple calculator application.")

    # Create main.py and render.py files to support the tests
    main_py = """
import sys
from pkg.calculator import calculate
from pkg.render import render_result

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py \"expression\"")
        print("Example: python main.py \"3 + 4 * 2\"")
        return
        
    expression = sys.argv[1]
    try:
        result = calculate(expression)
        print(render_result(expression, result))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
"""
    write_file("./calculator", "main.py", main_py)

    calculator_py = """
def calculate(expression):
    # Simple calculator implementation
    return eval(expression)
"""
    write_file("./calculator", "pkg/calculator.py", calculator_py)

    render_py = """
def render_result(expression, result):
    return f"Result of {expression} = {result}"
"""
    write_file("./calculator", "pkg/render.py", render_py)

    # Create __init__.py to make pkg a proper package
    write_file("./calculator", "pkg/__init__.py", "")

def call_function(function_call_part, verbose=False):
    """
    Handle function calls from the LLM.
    
    Args:
        function_call_part: A types.FunctionCall object with name and args properties
        verbose: Whether to print detailed information
        
    Returns:
        types.Content with the function response
    """
    function_name = function_call_part.name
    args = function_call_part.args if function_call_part.args else {}
    
    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")
    
    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    
    # Check if function exists
    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )
    
    # Add working_directory parameter
    args["working_directory"] = "./calculator"
    
    try:
        # Call the function with unpacked arguments
        function_result = functions[function_name](**args)
        
        # Return result as Content object
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result}
                )
            ]
        )
    except Exception as e:
        # Handle any exceptions during function execution
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing {function_name}: {str(e)}"}
                )
            ]
        )

def main():
    # Setup test environment to ensure files exist
    setup_test_environment()
    
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    
    model_name = "gemini-2.0-flash-001"

    verbose = "--verbose" in sys.argv
    if verbose:
        sys.argv.remove("--verbose")
    
    user_prompt = sys.argv[1] if len(sys.argv) > 1 else input("Enter your prompt: ")

    if verbose:
        print(f"User prompt: {user_prompt}")

    # Initialize conversation with user's prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    # Create a conversation loop with a maximum of 20 iterations
    max_iterations = 20
    for i in range(max_iterations):
        try:
            # Send the current conversation to the model
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                ),
            )
            
            # Get the latest response
            if not response.candidates or not response.candidates[0].content:
                print("No response generated.")
                break
            
            latest_candidate = response.candidates[0]
            
            # Add model's response to conversation history
            messages.append(latest_candidate.content)
            
            # Check if this is a function call or a final text response
            function_called = False
            if hasattr(latest_candidate.content, 'parts'):
                for part in latest_candidate.content.parts:
                    # Check if part has a function_call and that the function_call has a name attribute
                    if (part and hasattr(part, 'function_call') and 
                        part.function_call is not None and 
                        hasattr(part.function_call, 'name')):
                        
                        function_called = True
                        # Execute the function
                        function_call_result = call_function(part.function_call, verbose)
                        
                        # Add function result to conversation
                        messages.append(function_call_result)
            
            # If no function was called, this is the final response
            if not function_called:
                # Make sure text attribute exists before trying to print it
                if hasattr(latest_candidate.content, 'text'):
                    print("Final response:")
                    print(latest_candidate.content.text)
                else:
                    print("Final response (no text content):")
                    print(latest_candidate.content)
                break
                
        except Exception as e:
            print(f"Error during conversation: {str(e)}")
            import traceback
            traceback.print_exc()  # Print the full traceback for debugging
            break
    
    # If we've reached max iterations without a final response
    if i == max_iterations - 1:
        print("Reached maximum number of conversation turns without a final response.")
    
    if verbose and hasattr(response, 'usage_metadata'):
        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count
        print(f"\nPrompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")


if __name__ == "__main__":
    main()
