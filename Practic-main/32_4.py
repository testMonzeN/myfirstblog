'''
Вам дана последовательность строк.
Выведите строки, содержащие обратный слеш "\﻿".
Sample Input:

\w denotes word character
No slashes here
Sample Output:

\w denotes word character
'''
import sys
list = []

for line in sys.stdin:
    pattern = r'\\'
    line = line.rstrip()

    if '\\' in line:
        list.append(line)

print(*list, sep='\n')

# изи