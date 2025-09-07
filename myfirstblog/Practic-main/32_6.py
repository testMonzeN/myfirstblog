'''
Вам дана последовательность строк.
В каждой строке замените все вхождения подстроки "human" на подстроку "computer"﻿ и выведите полученные строки.

Sample Input:

I need to understand the human mind
humanity
Sample Output:

I need to understand the computer mind
computerity
'''

import sys
import re

list = []
count = 0
for line in sys.stdin:
    pattern = r'(\w+)\1'
    line = line.rstrip()

    try: list.append(line.replace('human', 'computer'))
    except:list.append(line.replace('computer', 'human'))

print(*list, sep='\n')
# подумал началась хорошая жизнь