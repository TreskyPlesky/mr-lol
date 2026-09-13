
import os
from functions.write_file import write_file

result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(result1)
print(result2)
print(result3)
