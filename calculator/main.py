import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Calculator App")
        print("Usage: python main.py \"<expression>\"")
        print("Example: python main.py \"3 + 5\"")
    else:
        expression = sys.argv[1]
        try:
            result = eval(expression)
            print(result)
        except Exception as e:
            print(f"Error: {e}")