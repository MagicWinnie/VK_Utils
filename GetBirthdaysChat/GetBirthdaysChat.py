"""
Getting peoples' birthday into a table
By @MagicWinnie
"""
import os
import json
import pandas as pd
import vk_api
from argparse import ArgumentParser


print("[WARNING] This script currently does not work due to VK limitations.")


def auth_handler(remember_device: bool = True):
    key = input("Enter authentication code: ")
    return key, remember_device


parser = ArgumentParser()
parser.add_argument(
    "chatID",
    type=int,
    help="Chat ID"
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
    default="birthdays.csv",
    help="output file name (default: birthdays.csv)",
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
CHAT_ID = args.chatID

vk_session = vk_api.VkApi(
    login=LOGIN, password=PASSWORD,
    auth_handler=auth_handler
)
vk_session.auth(token_only=True)
vk = vk_session.get_api()

d = dict(vk.messages.getChat(chat_id=CHAT_ID))

if d == {}:
    print("[ERROR] No users found")
    exit(-1)

users_info = vk.users.get(user_ids=d["users"], fields="bdate")
ids = [x["id"] for x in users_info]
first_names = [x["first_name"] for x in users_info]
last_names = [x["last_name"] for x in users_info]
bdates = []

for x in users_info:
    try:
        bdates.append(x["bdate"])
    except:
        bdates.append(None)

df_dict = {
    "id": ids,
    "first_name": first_names,
    "last_name": last_names,
    "bdate": bdates,
}
df = pd.DataFrame(df_dict)
df.to_csv(args.output, index=False)
