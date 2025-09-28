
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
