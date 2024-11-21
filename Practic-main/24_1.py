'''
Вам дается текстовый файл, содержащий некоторое количество непустых строк.
На основе него сгенерируйте новый текстовый файл, содержащий те же строки в обратном порядке.

Пример входного файла:
ab
c
dde
ff

﻿Пример выходного файла:
ff
dde
c
ab

УВЫ, ДАТЬ ССЫЛКУ НА ФАЙЛ НЕ МОГУ, ОНИ РАЗНЫЕ ВСЕ
'''


replText = []
with open('dataset_24465_4.txt') as file, open('copy.txt', 'a') as copyFile:
    for text in file:
        text = text.rstrip()
        replText.append(text)

    replText.reverse()
    for text in replText:
        copyFile.write(text + '\n')
