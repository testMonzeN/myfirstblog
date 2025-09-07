'''
ссылка на файл - https://stepik.org/media/attachments/lesson/24465/main.zip
ссылка на пример архива - https://stepik.org/media/attachments/lesson/24465/sample.zip
ссылка на пример ответа - https://stepik.org/media/attachments/lesson/24465/sample_ans.txt


Вам дана в архиве (ссылка) файловая структура, состоящая из директорий и файлов.

Вам необходимо распаковать этот архив, и затем найти в данной в файловой структуре все директории, в которых есть хотя бы один файл с расширением ".py". 

Ответом на данную задачу будет являться файл со списком таких директорий, отсортированных в лексикографическом порядке.

Для лучшего понимания формата задачи, ознакомьтесь с примером.
Пример архива 
Пример ответа
'''


import os

with open('lesson2.txt', 'a') as lesson:
    for current_dir, dirs, files in os.walk('main'):
        file_path = os.listdir(current_dir)

        for i in file_path:
            if i.endswith('.py'):
                print(current_dir)
                break