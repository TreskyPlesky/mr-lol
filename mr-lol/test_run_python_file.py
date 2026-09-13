import os
from functions.run_python_file import run_python_file
import calculator
result1 = run_python_file("calculator", "main.py")
result2 = run_python_file("calculator", "main.py", ["3 + 5"])
result3 = run_python_file("calculator", "tests.py")
result4 = run_python_file("calculator", "../main.py")
result5 = run_python_file("calculator", "nonexistent.py")
result6 = run_python_file("calculator", "lorem.txt")
print(result1)
print(result2)
print(result3)
print(result4)
print(result5)
print(result6)
