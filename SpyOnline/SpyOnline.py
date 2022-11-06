import os
import time
import json
import pandas as pd
import requests
from argparse import ArgumentParser
from datetime import datetime
import vk_api


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


parser = ArgumentParser()
parser.add_argument(
    "-u", "--users",
    nargs="+", help="User IDs", required=True
)
parser.add_argument(
    "--delay",
    type=int,
    default=5 * 60,
    help="delay in seconds between callbacks",
)
parser.add_argument(
    "--login",
    type=str,
    default="../LoginData/login.json",
    help="path to login.json (default: ../LoginData/login.json)",
)
parser.add_argument(
    "--output",
    type=str,
    default="OnlineUsers.csv",
    help="where to save csv file",
)
args = parser.parse_args()

assert os.path.isfile(args.login),\
    "[ERROR] {} is not a file or it does not exist!".format(args.login)
with open(args.login, "r") as f:
    j = json.load(f)

assert "login" in j, "[ERROR] `login` key does not exist!"
assert "pass" in j, "[ERROR] `pass` key does not exist!"
LOGIN = j["login"]
PASSWORD = j["pass"]
vk_session = vk_api.VkApi(
    login=LOGIN, password=PASSWORD,
    auth_handler=auth_handler
)
vk_session.auth(token_only=True)
vk = vk_session.get_api()

if os.path.isfile(args.output):
    df = pd.read_csv(args.output, encoding="utf-8")
else:
    df = pd.DataFrame(
        columns=["time", "id", "first_name", "last_name", "city", "online"])

errorCnt = 0
delay = args.delay  # in sec
startTime = time.time()
while True:
    if errorCnt > 5:
        print("[ERROR] No internet connection...")
        break
    try:
        data = vk.users.get(
            user_ids=",".join(args.users),
            fields="sex,city,country,online,last_seen",
        )
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[INFO]", currentTime)
        for p in data:
            df.loc[len(df)] = [currentTime, p["id"], p["first_name"],  # type: ignore
                               p["last_name"], p["city"]["title"] if "city" in p else "", p["online"]]
        time.sleep(delay - ((time.time() - startTime) % delay))
        errorCnt = 0
    except KeyboardInterrupt:
        break
    except requests.ConnectionError:
        errorCnt += 1
        print("[WARNING] Trying to reconnect... Attempt #{}".format(errorCnt))

df.to_csv(args.output, encoding="utf-8", index=False)
