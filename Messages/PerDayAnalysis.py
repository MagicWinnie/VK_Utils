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

# 0 - All messages per date
# 1 - Messages per speaker per date
# 2 - All messages per time of day
# 3 - Messages per speaker per time of day
# 4 - All messages per hour 
# 5 - Messages per speaker per hour

if len(sys.argv) != 3:
    print("USAGE: python3 PerDayAnalysis.py <folder> <type>")
    exit(-1)

DATA_FOLDER = sys.argv[1]
TYPE = int(sys.argv[2])

assert TYPE in range(6)

def process_string(s: str) -> str:
    s = s.strip()
    s = s.replace('\n', '')
    return s

def return_key(c: collections.Counter) -> str:
    return c[0]

# TIME = (start, end) => start <= TIME < END
MORNING = (7, 12)
DAY     = (12, 18)
EVENING = (18, 0)
NIGHT   = (0, 7)

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

if TYPE == 0:
    fig, ax = plt.subplots()
    c = collections.Counter()

    for m in messages:
        t = m.split()
        c[datetime.strptime(t[-1][:-1], '%d/%m/%Y')] += 1

    ax.plot(c.keys(), c.values(), 'o', markersize=3)
    ax.grid()
    ax.set_xlabel("Date")
    ax.set_ylabel("Messages")
    ax.set_title("All messages per date")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=100))
    plt.gcf().autofmt_xdate()

if TYPE == 1:
    fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True)

    c1 = collections.Counter()
    c2 = collections.Counter()
    for m in messages:
        t = m.split()
        if t[0] + " " + t[1] == speakers[0]:
            c1[datetime.strptime(t[-1][:-1], '%d/%m/%Y')] += 1
        else:
            c2[datetime.strptime(t[-1][:-1], '%d/%m/%Y')] += 1

    ax[0].plot(c1.keys(), c1.values(), 'o', color='blue', markersize=3)
    ax[1].plot(c2.keys(), c2.values(), 'o', color='red', markersize=3)

    fig.suptitle("Messages per speaker per date")
    ax[0].set_xlabel("Date")
    ax[0].set_ylabel("Messages")
    ax[0].set_title(speakers[0])
    ax[0].grid()
    ax[1].set_xlabel("Date")
    ax[1].set_title(speakers[1])
    ax[1].grid()
    fig.tight_layout()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=100))
    plt.gcf().autofmt_xdate()

if TYPE == 2:
    fig, ax = plt.subplots()
    c = collections.Counter()

    for m in messages:
        t = m.split()
        time = datetime.strptime(t[-2][1:], '%H:%M:%S')
        if time.hour >= NIGHT[0] and time.hour < NIGHT[1]:
            c['NIGHT'] += 1
        elif time.hour >= MORNING[0] and time.hour < MORNING[1]:
            c['MORNING'] += 1
        elif time.hour >= DAY[0] and time.hour < DAY[1]:
            c['DAY'] += 1
        else:
            c['EVENING'] += 1

    ax.bar(c.keys(), c.values())
    
    ax.set_xlabel("Time of day")
    ax.set_ylabel("Messages")
    ax.set_title("All messages per time of day")

if TYPE == 3:
    fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True)

    c1 = collections.Counter()
    c2 = collections.Counter()
    for m in messages:
        t = m.split()
        time = datetime.strptime(t[-2][1:], '%H:%M:%S')
        if t[0] + " " + t[1] == speakers[0]:
            if time.hour >= NIGHT[0] and time.hour < NIGHT[1]:
                c1['NIGHT'] += 1
            elif time.hour >= MORNING[0] and time.hour < MORNING[1]:
                c1['MORNING'] += 1
            elif time.hour >= DAY[0] and time.hour < DAY[1]:
                c1['DAY'] += 1
            else:
                c1['EVENING'] += 1
        else:
            if time.hour >= NIGHT[0] and time.hour < NIGHT[1]:
                c2['NIGHT'] += 1
            elif time.hour >= MORNING[0] and time.hour < MORNING[1]:
                c2['MORNING'] += 1
            elif time.hour >= DAY[0] and time.hour < DAY[1]:
                c2['DAY'] += 1
            else:
                c2['EVENING'] += 1

    ax[0].bar(c1.keys(), c1.values(), color='blue')
    ax[1].bar(c2.keys(), c2.values(), color='red')

    fig.suptitle("Messages per speaker per time of day")

    ax[0].set_xlabel("Time of day")
    ax[0].set_ylabel("Messages")
    ax[0].set_title(speakers[0])

    ax[1].set_xlabel("Time of day")
    ax[1].set_title(speakers[1])
    fig.tight_layout()

if TYPE == 4:
    fig, ax = plt.subplots()
    c = collections.Counter()

    for m in messages:
        t = m.split()
        time = datetime.strptime(t[-2][1:], '%H:%M:%S')
        c[time.hour] += 1
        
    ax.bar(c.keys(), c.values())
    
    ax.set_xlabel("Hour")
    ax.set_ylabel("Messages")
    ax.set_title("All messages per hour ")

if TYPE == 5:
    fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True)

    c1 = collections.Counter()
    c2 = collections.Counter()
    for m in messages:
        t = m.split()
        time = datetime.strptime(t[-2][1:], '%H:%M:%S')
        if t[0] + " " + t[1] == speakers[0]:
            c1[time.hour] += 1
        else:
            c2[time.hour] += 2

    ax[0].bar(c1.keys(), c1.values(), color='blue')
    ax[1].bar(c2.keys(), c2.values(), color='red')

    fig.suptitle("Messages per speaker per hour")

    ax[0].set_xlabel("Hour")
    ax[0].set_ylabel("Messages")
    ax[0].set_title(speakers[0])

    ax[1].set_xlabel("Hour")
    ax[1].set_title(speakers[1])
    fig.tight_layout()

plt.show()
    