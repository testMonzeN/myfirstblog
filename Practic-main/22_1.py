'''

В первой строке дано три числа, соответствующие некоторой дате date -- год, месяц и день.
Во второй строке дано одно число days -- число дней.

Вычислите и выведите год, месяц и день даты, которая наступит, когда с момента исходной даты date пройдет число дней, равное days.

Примечание:
Для решения этой задачи используйте стандартный модуль datetime.
Вам будут полезны класс datetime.date для хранения даты и класс datetime.timedelta﻿ для прибавления дней к дате.

Sample Input 1:

2016 4 20
14
Sample Output 1:

2016 5 4
Sample Input 2:

2016 2 20
9
Sample Output 2:

2016 2 29
Sample Input 3:

2015 12 31
1
Sample Output 3:

2016 1 1

'''



# вариант 1 (поверхностно почитал документацию)

import datetime

year, month, day1 = input().split()
day2 = int(input())

date = datetime.date(int(year), int(month), int(day1))
delta = datetime.timedelta(days=int(day2))

correct_data = date+delta
formatted_date = correct_data.strftime('%Y %m %d')

string = formatted_date.split()

year2 = string[0]
month2 = string[1].replace("01", "1").replace("02", "2").replace("03", "3").replace("04", "4").replace("05", "5").replace("06", "6").replace("07", "7").replace("08", "8").replace("09", "9").replace("00", "0")
day3 = string[2].replace("01", "1").replace("02", "2").replace("03", "3").replace("04", "4").replace("05", "5").replace("06", "6").replace("07", "7").replace("08", "8").replace("09", "9").replace("00", "0")

print(year2, month2, day3)




# вариант 2 (сгорело, не поверил что вариант 1 норм код и перечитал документацию, понял что я балван, и я переделал задание)

from datetime import date, timedelta

year, month, day = map(int, input().split())
days = int(input())

start_date = date(year, month, day)

result_date = start_date + timedelta(days=days)

print(result_date.year, result_date.month, result_date.day)
