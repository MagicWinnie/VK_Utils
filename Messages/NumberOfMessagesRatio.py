'''
Analyze amount of messages with a person
* Requires downloading a .zip archive with messages through VKOpt
as working with messages through VK API became nearly impossible
* Save the file with following parameters (with all whitespaces):
`Message format`: 
%username% (%date%)

`Date format`:
HH:MM:ss  dd/mm/yyyy
* Put the .txt files into `data` folder next to the script
By @MagicWinnie
'''

import os
import sys
from datetime import datetime
import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 1 - Messages per speaker per date

if len(sys.argv) != 2:
    print("USAGE: python3 PerDayAnalysis.py <folder>")
    exit(-1)

DATA_FOLDER = sys.argv[1]

def process_string(s: str) -> str:
    s = s.strip()
    s = s.replace('\n', '')
    return s

def return_key(c: collections.Counter) -> str:
    return c[0]

messages = []
speakers = collections.Counter()

import platform
delimeter = '\\' if platform.system() == "Windows" else '/'
FOLDER = delimeter.join(os.path.realpath(__file__).split(delimeter)[:-1])
    
FILES = os.listdir(os.path.join(FOLDER, DATA_FOLDER))
for f in FILES:
    with open(os.path.join(FOLDER, DATA_FOLDER, f), 'r', encoding='utf-8') as f_b:
        messages += list(map(process_string, f_b.readlines()))
        speakers[messages[-1].split()[0] + " " + messages[-1].split()[1]] += 1

speakers = list(map(return_key, speakers.most_common(2)))


fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True)

c1 = collections.Counter()
c2 = collections.Counter()
for m in messages:
    t = m.split()
    if t[0] + " " + t[1] == speakers[0]:
        c1[datetime.strptime(t[-1][:-1], '%d/%m/%Y')] += 1
    else:
        c2[datetime.strptime(t[-1][:-1], '%d/%m/%Y')] += 1

data = []
INVERT = True
for i in c1.keys():
    if c2[i] != 0:
        if INVERT:
            data.append(c2[i] / c1[i])
        else:
            data.append(c1[i] / c2[i])
    else:
        data.append(float('nan'))
if INVERT:
    TEXT = f"{speakers[1]}/{speakers[0]}"
else:
    TEXT = f"{speakers[0]}/{speakers[1]}"

ax.plot(c1.keys(), data, 'o', color='blue')
ax.axhline(y=1, color='r', linestyle='-')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=100))
plt.gcf().autofmt_xdate()
fig.suptitle("Messages per speaker per date")
ax.set_xlabel("Date")
ax.set_ylabel("Ratio")
ax.set_title(TEXT)
plt.show()