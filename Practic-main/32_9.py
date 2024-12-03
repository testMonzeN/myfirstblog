'''
Вам дана последовательность строк.
В каждой строке замените все вхождения нескольких одинаковых букв на одну букву.
Буквой считается символ из группы \w.
Sample Input:

attraction
buzzzz
Sample Output:

atraction
buz
'''

import re
import sys

for line in sys.stdin:
    pattern = r'(\w)\1+' # тут я пронял что пошел куда то не тудаi
    line = line.rstrip()

    s = re.sub(pattern, r'\1', line)
    print(s)

# плакал пока делал