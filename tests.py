import os
import shutil
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def setup_test_environment():
    # Create calculator directory and its subdirectories
    os.makedirs("calculator/pkg", exist_ok=True)
    
    # Create main.py with calculator code
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
    write_file("calculator", "main.py", main_py)
    
    # Create calculator.py implementation
    calculator_py = """
def calculate(expression):
    # Simple calculator implementation
    return eval(expression)
"""
    write_file("calculator", "pkg/calculator.py", calculator_py)
    
    # Create render.py implementation
    render_py = """
def render_result(expression, result):
    return f"Result of {expression} = {result}"
"""
    write_file("calculator", "pkg/render.py", render_py)
    
    # Create tests.py in calculator directory
    tests_py = """
print("Running calculator tests...")
from pkg.calculator import calculate

assert calculate("1 + 1") == 2
assert calculate("2 * 3") == 6

print("All tests passed!")
"""
    write_file("calculator", "tests.py", tests_py)
    
    # Create __init__.py files to make pkg a proper package
    write_file("calculator", "pkg/__init__.py", "")

def cleanup_test_environment():
    # Remove the test calculator directory
    if os.path.exists("calculator"):
        shutil.rmtree("calculator")

def test_run_python_file():
    try:
        setup_test_environment()
        
        # Test running a Python file with no arguments
        print("run_python_file(\"calculator\", \"main.py\"):")
        print(run_python_file("calculator", "main.py"))
        print("\n" + "-"*50 + "\n")
        
        # Test running a Python file with arguments
        print("run_python_file(\"calculator\", \"main.py\", [\"3 + 5\"]):")
        print(run_python_file("calculator", "main.py", ["3 + 5"]))
        print("\n" + "-"*50 + "\n")
        
        # Test running tests.py
        print("run_python_file(\"calculator\", \"tests.py\"):")
        print(run_python_file("calculator", "tests.py"))
        print("\n" + "-"*50 + "\n")
        
        # Test attempting to run a file outside working directory
        print("run_python_file(\"calculator\", \"../main.py\"):")
        print(run_python_file("calculator", "../main.py"))
        print("\n" + "-"*50 + "\n")
        
        # Test attempting to run a non-existent file
        print("run_python_file(\"calculator\", \"nonexistent.py\"):")
        print(run_python_file("calculator", "nonexistent.py"))
        
    finally:
        cleanup_test_environment()

if __name__ == "__main__":
    test_run_python_file()