'''
Вам дана последовательность строк.
Выведите строки, содержащие две буквы "z﻿", между которыми ровно три символа.
Sample Input:

zabcz
zzz
zzxzz
zz
zxz
zzxzxxz
Sample Output:

zabcz
zzxzz
'''
#оно пропало але

import sys
import re

for line in sys.stdin:
    pattern = r'z.{3}z'
    line = line.rstrip()

    if re.findall(pattern, line) != []:
        print(line)

#восстановил



