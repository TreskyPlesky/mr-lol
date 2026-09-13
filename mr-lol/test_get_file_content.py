
import os
from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")
result2 = get_file_content("calculator", "main.py")
result3 = get_file_content("calculator", "pkg/calculator.py")
result4 = get_file_content("calculator", "/bin/cat")
result5 = get_file_content("calculator", "pkg/does_not_exist.py")
print(result2)
print(result3)
print(result4)
print(result5)
