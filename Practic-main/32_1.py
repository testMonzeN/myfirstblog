'''
Вам дана последовательность строк.
Выведите строки, содержащие "cat" в качестве подстроки хотя бы два раза.

Примечание:
Считать все строки по одной из стандартного потока ввода вы можете, например, так

import sys

for line in sys.stdin:
    line = line.rstrip()
    # process line

Sample Input:

catcat
cat and cat
catac
cat
ccaatt
Sample Output:

catcat
cat and cat
'''

import re
import sys
list = []

for line in sys.stdin:
    line = line.rstrip()
    search = 'cat'

    s = re.findall(search, line)
    if len(s) > 1:
        list.append(line)

print(*list, sep='\n')

# изи