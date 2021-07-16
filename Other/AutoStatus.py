"""
Having timer in VK status 
By @MagicWinnie
"""

import os
import time
import datetime
import json
import vk_api
import requests
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("text", type=str, help="Event text")
parser.add_argument("date", type=datetime.date.fromisoformat, help="Event date")
parser.add_argument(
    "--login",
    type=str,
    default="../LoginData/login.json",
    help="path to login.json (default: ../LoginData/login.json)",
)
parser.add_argument(
    "--delay",
    type=int,
    default=10,
    help="delay between status updates (default: 10)",
)
args = parser.parse_args()


def auth_handler(remember_device: bool = True):
    key = input("Enter authentication code: ")
    return key, remember_device

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

def right_ending(m, t):
    endings = {
        "m": ["минута", "минуты", "минут"],
        "d": ["день", "дня", "дней"],
        "h": ["час", "часа", "часов"],
        "s": ["секунда", "секунды", "секунд"],
    }
    if m % 10 == 1 and m % 100 != 11:
        return str(m) + " " + endings[t][0]
    if m % 10 in (2, 3, 4) and m % 100 not in (12, 13, 14):
        return str(m) + " " + endings[t][1]
    return str(m) + " " + endings[t][2]


def dateDiffInSeconds(d1, d2):
    time_d = d2 - d1
    return time_d.days * 24 * 3600 + time_d.seconds


def secs2dhm(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes, seconds)


def runner(NOW, END_DATE):
    global args
    TEXT = "До {} осталось: {} {} {} {}"

    d, h, m, s = secs2dhm(dateDiffInSeconds(NOW, END_DATE))
    text = TEXT.format(
        args.text,
        right_ending(d, "d"),
        right_ending(h, "h"),
        right_ending(m, "m"),
        right_ending(s, "s"),
    )

    return text


assert os.path.isfile(args.login), "[ERROR] {} is not a file or it does not exist!".format(args.login)
with open(args.login, "r") as f:
    j = json.load(f)

assert "login" in j, "[ERROR] `login` key does not exist!"
assert "pass" in j, "[ERROR] `pass` key does not exist!"
login = j["login"]
password = j["pass"]

vk_session = vk_api.VkApi(login=login, password=password, auth_handler=auth_handler, captcha_handler=captcha_handler)
try:
    vk_session.auth()
except requests.ConnectionError:
    print("[ERROR] No internet connection")
    exit(-1)
except Exception as e:
    print("[ERROR] " + str(e))
    exit(-1)
vk = vk_session.get_api()

END_DATE = args.date
try:
    END_DATE.hour
except AttributeError:
    END_DATE = datetime.datetime.combine(END_DATE, datetime.time(0, 0))
DELAY = args.delay
NOW = datetime.datetime.now()
PREV = time.time()
TRIES = 0
print("[INFO] INIT FINISHED")
while END_DATE > NOW:
    if TRIES > 5:
        break
    if time.time() - PREV >= DELAY:
        text = runner(NOW, END_DATE)
        try:
            vk.status.set(text=text)
        except ConnectionError:
            print("[ERROR] No internet connection")
            TRIES += 1
        NOW = datetime.datetime.now()
        PREV = time.time()
print("[INFO] TIMER FINISHED")
