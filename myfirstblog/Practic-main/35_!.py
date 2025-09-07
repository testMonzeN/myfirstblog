'''
В этой задаче вам необходимо воспользоваться API сайта numbersapi.com

Вам дается набор чисел. Для каждого из чисел необходимо узнать, существует ли интересный математический факт об этом числе.

Для каждого числа выведите Interesting, если для числа существует интересный факт, и Boring иначе.
Выводите информацию об интересности чисел в таком же порядке, в каком следуют числа во входном файле.

Пример запроса к интересному числу:
http://numbersapi.com/31/math?json=true

Пример запроса к скучному числу:
http://numbersapi.com/999/math?json=true

Пример входного файла:
31
999
1024
502

﻿Пример выходного файла:
Interesting
Boring
Interesting
Boring
'''


import requests, json

with open('dataset_24476_3 (2).txt', mode='r+') as f:
    text = f.read().split()
    
    for line in text:
        api_url = f'http://numbersapi.com/{line}/math?json=true'

        res = requests.get(api_url, timeout = 5).json()

        try:
            if res['found'] == True:
                print('Interesting')
            else:
                print('Boring')
        except:
            print('Interesting')

