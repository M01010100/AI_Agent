import os
import shutil
from functions.get_file_content import get_file_content

def setup_test_environment():
    # Create calculator directory and its subdirectories
    os.makedirs("calculator/pkg", exist_ok=True)
    
    # Create test files with the REQUIRED content
    with open("calculator/main.py", "w") as f:
        f.write("# Test main.py file\n\ndef main():\n    print('Hello, world!')\n\nif __name__ == '__main__':\n    main()")
        
    with open("calculator/pkg/calculator.py", "w") as f:
        f.write("# Test calculator.py file\nclass Calculator:\n    def _apply_operator(self, operators, values):\n        return operators[0](values[0], values[1])")
    
    # Create a large lorem ipsum file
    with open("calculator/lorem.txt", "w") as f:
        # Generate a large text (over 20,000 characters)
        lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 500
        f.write(lorem_ipsum)

def cleanup_test_environment():
    # Remove the test calculator directory
    if os.path.exists("calculator"):
        shutil.rmtree("calculator")

def test_get_file_content():
    try:
        setup_test_environment()
        
        # Test reading a regular file
        print("get_file_content(\"calculator\", \"main.py\"):")
        print("Result:")
        print(get_file_content("calculator", "main.py"))
        print("\n" + "-"*50 + "\n")
        
        # Test reading a file in a subdirectory
        print("get_file_content(\"calculator\", \"pkg/calculator.py\"):")
        print("Result:")
        print(get_file_content("calculator", "pkg/calculator.py"))
        print("\n" + "-"*50 + "\n")
        
        # Test attempting to read a file outside working directory
        print("get_file_content(\"calculator\", \"/bin/cat\"):")
        print("Result:")
        print(get_file_content("calculator", "/bin/cat"))
        print("\n" + "-"*50 + "\n")
        
        # Test attempting to read a non-existent file
        print("get_file_content(\"calculator\", \"pkg/does_not_exist.py\"):")
        print("Result:")
        print(get_file_content("calculator", "pkg/does_not_exist.py"))
        
    finally:
        cleanup_test_environment()

if __name__ == "__main__":
    test_get_file_content()