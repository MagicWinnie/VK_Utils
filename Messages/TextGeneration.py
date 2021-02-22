'''
Generates random text from messages with a person
* Requires downloading a .zip archive with messages through VKOpt
as working with messages through VK API became nearly impossible
* Save the file with following parameters:
`Message format`: %message% 
`Date format`:    HH:MM:ss  dd/mm/yyyy
* Put the .txt files into `data` folder next to the script
By @MagicWinnie
'''

import os
import random

def process_string(s: str) -> str:
    s = s.strip()
    s = s.replace('\n', '')
    # s = s.lower()
    # s = ''.join([i for i in s if i.isalpha() or i == ' '])
    return s

def split(s: str) -> list:
    return s.split()

messages = []
db_keys = []
db_values = []

FOLDER = '\\'.join(os.path.realpath(__file__).split('\\')[:-1])
DATA_FOLDER = 'data'
FILES = os.listdir(os.path.join(FOLDER, DATA_FOLDER))
for f in FILES:
    with open(os.path.join(FOLDER, DATA_FOLDER, f), 'r', encoding='utf-8') as f_b:
        temp = list(map(process_string, f_b.readlines()))
        temp = list(filter(None, temp))
        temp = list(map(split, temp))
        temp = [item for sublist in temp for item in sublist]
        messages += temp

for i in range(0, len(messages)):
    if i + 1 > len(messages) - 1 or i + 2  > len(messages) - 1: break
    db_keys.append((messages[i], messages[i + 1]))
    db_values.append(messages[i + 2])

ind = random.randint(0, len(db_keys) - 1)
to_find = (db_keys[ind][0], db_keys[ind][1])
print(to_find[0], to_find[1], end=' ')

for i in range(100):
    matches = []
    for j in range(len(db_keys)):
        if db_keys[j] == to_find: matches.append(db_values[j])
    if len(matches) == 0:
        print("STOPPING")
        break
    temp = matches[random.randint(0, len(matches) - 1)]
    print(temp, end=' ')
    to_find = (to_find[1], temp)
