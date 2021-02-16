'''
Having timer in VK status 
By @MagicWinnie
'''

import vk_api
import datetime 
import time

def right_ending(m):
    if m % 10 == 1 and m % 100 != 11:
        return 'минута'
    if m % 10 in (2, 3, 4) and m % 100 not in (12, 13, 14):
        return 'минуты'
    return 'минут'


with open('token.in', 'r') as f:
    token = f.readline()

vk = vk_api.VkApi(token=token)

# time zone offset
UTC = 7
# year, month, date, hour, minutes
END_DATE = datetime.datetime(2019, 6, 5, 14, 0, 0, 0)
# delay between updates, sec
DELAY = 60
# status text
TEXT = "До экзамена осталось: {} {}, а ты ничего не выучил"

while True:
    NOW = datetime.datetime.now()
    s = (END_DATE - NOW).total_seconds()
    minutes = s // 60
    vk.method("status.set", {"text": TEXT.format(minutes, right_ending(minutes))})
    time.sleep(DELAY)
    