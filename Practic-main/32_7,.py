'''
Вам дана последовательность строк.
В каждой строке замените первое вхождение слова, состоящего только из латинских букв "a" (регистр не важен), на слово "argh".

Примечание:
Обратите внимание на параметр count у функции sub.
Sample Input:

There’ll be no more "Aaaaaaaaaaaaaaa"
AaAaAaA AaAaAaA
Sample Output:

There’ll be no more "argh"
argh AaAaAaA
'''
import sys
import re

list = []
count = 0
for line in sys.stdin:
    pattern = r'\b[aA]+\b'
    line = line.rstrip()

    s = re.sub(pattern, 'argh', line, count=1)
    print(s)

# начал совниваться в своих словах