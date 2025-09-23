import os
import shutil
from functions.get_files_info import get_files_info

def setup_test_environment():
    os.makedirs("calculator/pkg", exist_ok=True)
    
    with open("calculator/main.py", "w") as f:
        f.write("# Test main.py file")
        
    with open("calculator/tests.py", "w") as f:
        f.write("# Test tests.py file")
        
    with open("calculator/pkg/calculator.py", "w") as f:
        f.write("# Test calculator.py file")
        
    with open("calculator/pkg/render.py", "w") as f:
        f.write("# Test render.py file")

def cleanup_test_environment():
    if os.path.exists("calculator"):
        shutil.rmtree("calculator")

def test_get_files_info():
    try:
        setup_test_environment()
        
        print("get_files_info(\"calculator\", \".\"):")
        print("Result for current directory:")
        print(get_files_info("calculator", "."))
        print()
        
        print("get_files_info(\"calculator\", \"pkg\"):")
        print("Result for 'pkg' directory:")
        print(get_files_info("calculator", "pkg"))
        print()
        
        print("get_files_info(\"calculator\", \"/bin\"):")
        print("Result for '/bin' directory:")
        print(get_files_info("calculator", "/bin"))
        print()
        
        print("get_files_info(\"calculator\", \"../\"):")
        print("Result for '../' directory:")
        print(get_files_info("calculator", "../"))
        
    finally:
        cleanup_test_environment()

if __name__ == "__main__":
    test_get_files_info()