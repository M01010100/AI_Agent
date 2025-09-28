import os
import shutil
from functions.write_file import write_file

def setup_test_environment():
    # Create calculator directory and its subdirectories
    os.makedirs("calculator/pkg", exist_ok=True)

def cleanup_test_environment():
    # Remove the test calculator directory
    if os.path.exists("calculator"):
        shutil.rmtree("calculator")

def test_write_file():
    try:
        setup_test_environment()
        
        # Test writing a file in the root directory
        print("write_file(\"calculator\", \"lorem.txt\", \"wait, this isn't lorem ipsum\"):")
        print("Result:")
        print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
        print("\n" + "-"*50 + "\n")
        
        # Test writing a file in a subdirectory
        print("write_file(\"calculator\", \"pkg/morelorem.txt\", \"lorem ipsum dolor sit amet\"):")
        print("Result:")
        print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
        print("\n" + "-"*50 + "\n")
        
        # Test attempting to write a file outside working directory
        print("write_file(\"calculator\", \"/tmp/temp.txt\", \"this should not be allowed\"):")
        print("Result:")
        print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
        
    finally:
        cleanup_test_environment()

if __name__ == "__main__":
    test_write_file()