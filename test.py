import os, re

def getFile():
    for item in os.listdir(os.getcwd() + '/Practic-main'):
        with open(os.getcwd() + '/Practic-main/' + item, mode='r') as file:
            text = file.read()
            start_index = text.index("'''") + len("'''")
            end_index = text.index("'''", start_index)

            print(item)
            print(text[start_index:end_index])


getFile()
