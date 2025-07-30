from functions.run_python_file import run_python_file

def run_tests():
    print('run_python_file("calculator", "main.py"):')
    print("Result for main.py:")
    print(run_python_file("calculator", "main.py"))
    print()

    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    print("Result for [3 + 5]:")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print('run_python_file("calculator", "tests.py"):')
    print("Result for tests.py:")
    print(run_python_file("calculator", "tests.py"))
    print()
    
    print('run_python_file("calculator", "../main.py"):')
    print("Result for '../main.py':")
    print(run_python_file("calculator", "../main.py"))
    print()

    print('run_python_file("calculator", "non_existent.py"):')
    print("Result for 'nonexistent.py':")
    print(run_python_file("calculator", "nonexistent.py"))
    print()


if __name__ == "__main__":
    run_tests()

