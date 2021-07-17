import os
import time
import json
import pandas as pd
import requests
from vk_messages import MessagesAPI
from argparse import ArgumentParser
from datetime import datetime

parser = ArgumentParser()
parser.add_argument("-u", "--users", nargs="+", help="User IDs", required=True)
parser.add_argument(
    "--delay",
    type=int,
    default=5 * 60,
    help="delay between callbacks",
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

assert os.path.isfile(args.login), "[ERROR] {} is not a file or it does not exist!".format(args.login)
with open(args.login, "r") as f:
    j = json.load(f)

assert "login" in j, "[ERROR] `login` key does not exist!"
assert "pass" in j, "[ERROR] `pass` key does not exist!"
LOGIN = j["login"]
PASSWORD = j["pass"]
messages = MessagesAPI(login=LOGIN, password=PASSWORD, two_factor=True)

if os.path.isfile(args.output):
    df = pd.read_csv(args.output, encoding="utf-8")
else:
    df = pd.DataFrame(columns=["time", "id", "first_name", "last_name", "city", "online"])

errorCnt = 0
delay = args.delay # in sec
startTime = time.time()
while True:
    if errorCnt > 5:
        print("[ERROR] No internet connection...")
        break
    try:
        data = messages.method(
            "users.get",
            user_ids=",".join(args.users),
            fields="sex,city,country,online,last_seen",
        )
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[INFO]", currentTime)
        for p in data:
            df.loc[len(df)] = [currentTime, p["id"], p["first_name"], p["last_name"], p["city"]["title"], p["online"]]
        time.sleep(delay - ((time.time() - startTime) % delay))
    except KeyboardInterrupt:
        break
    except requests.ConnectionError:
        errorCnt += 1
    except Exception as e:
        print("[ERROR] {}".format(e))
        break

df.to_csv(args.output, encoding="utf-8", index=False)
