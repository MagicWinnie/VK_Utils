'''
Having timer in VK status 
By @MagicWinnie
'''

import vk_api
import datetime 
import json
import time
import os

def auth_handler(remember_device: bool=True)->(str, bool):
    key = input("Enter authentication code: ")
    return key, remember_device

def right_ending(m, t):
    endings = {
        'm': ['минута', 'минуты', 'минут'],
        'd': ['день', 'дня', 'дней'],
        'h': ['час', 'часа', 'часов'],
        's': ['секунда', 'секунды', 'секунд']
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
    return (days, hours, minutes, seconds)

def runner(NOW, END_DATE):
    EVENT = ""
    TEXT = "До {} осталось: {} {} {} {}"
    
    d, h, m, s = secs2dhm(dateDiffInSeconds(NOW, END_DATE))
    text = TEXT.format(EVENT, right_ending(d, 'd'), right_ending(h, 'h'), right_ending(m, 'm'), right_ending(s, 's'))
    
    return text

import platform
if platform.system() == "Windows":
    FOLDER = '\\'.join(os.path.realpath(__file__).split('\\')[:-1])
else:
    FOLDER = '/'.join(os.path.realpath(__file__).split('/')[:-1])
    
j = json.load(open(os.path.join(FOLDER, 'login.json'), 'r'))

login = j['login']
password = j['pass']
user_id = j['user_id']

vk_session = vk_api.VkApi(login=login, password=password, auth_handler=auth_handler)
vk_session.auth()
vk = vk_session.get_api()

# time zone offset
UTC = 7
# year, month, date, hour, minutes
END_DATE = datetime.datetime(2021, 8, 10, 0, 0, 0, 0)
# delay between updates, sec
DELAY = 10

NOW = datetime.datetime.now()
PREV = time.time()

print("[INFO] INIT FINISHED")

while END_DATE > NOW:
    if time.time() - PREV >= DELAY:
        text = runner(NOW, END_DATE)
        vk.status.set(text=text)
        NOW = datetime.datetime.now()
        PREV = time.time()
