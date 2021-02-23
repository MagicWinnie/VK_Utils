'''
Having timer in VK status 
By @MagicWinnie
'''

import vk_api
import datetime 
import time
import os

def right_ending(m, t):
    endings = {
        'm': ['минута', 'минуты', 'минут'],
        'd': ['день', 'дня', 'дней'],
        'h': ['час', 'часа', 'часов']
    }
    if m % 10 == 1 and m % 100 != 11:
        return str(m) + ' ' + endings[t][0]
    if m % 10 in (2, 3, 4) and m % 100 not in (12, 13, 14):
        return str(m) + ' ' + endings[t][1]
    return str(m) + ' ' + endings[t][2]

def dateDiffInSeconds(d1, d2):
    time_d = d2 - d1
    return time_d.days * 24 * 3600 + time_d.seconds

def secs2dhm(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes)

import platform
if platform.system() == "Windows":
    FOLDER = '\\'.join(os.path.realpath(__file__).split('\\')[:-1])
else:
    FOLDER = '/'.join(os.path.realpath(__file__).split('/')[:-1])
    
with open(os.path.join(FOLDER, 'token.in'), 'r') as f:
    token = f.readline()

vk = vk_api.VkApi(token=token)

# time zone offset
UTC = 7
# year, month, date, hour, minutes
END_DATE = datetime.datetime(2021, 8, 10, 0, 0, 0, 0)
# delay between updates, sec
DELAY = 60
# status text
EVENT = ""
TEXT = "До {} осталось: {} {} {} "

NOW = datetime.datetime.now()
PREV = time.time()

while END_DATE > NOW:
    if time.time() - PREV >= 60:
        d, h, m = secs2dhm(dateDiffInSeconds(NOW, END_DATE))
        vk.method("status.set", {"text": TEXT.format(EVENT, right_ending(d, 'd'), right_ending(h, 'h'), right_ending(m, 'm')), "v": "5.130"})
        NOW = datetime.datetime.now()
        PREV = time.time()

vk.method("status.set", {"text": "Готово"})