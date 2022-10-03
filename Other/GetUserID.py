"""
Get user ID
"""
import os
import json
from argparse import ArgumentParser
import vk_api


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device


parser = ArgumentParser()
parser.add_argument("screenName", type=str, help="Screen name")
parser.add_argument(
    "--login",
    type=str,
    default="../LoginData/login.json",
    help="path to login.json (default: ../LoginData/login.json)",
)
args = parser.parse_args()

if args.screenName[:2] == "id" and args.screenName[2:].isdigit():
    print(args.screenName[2:])
    exit(0)

assert os.path.isfile(
    args.login
), "[ERROR] {} is not a file or it does not exist!".format(args.login)
with open(args.login, "r") as f:
    j = json.load(f)

assert "login" in j, "[ERROR] `login` key does not exist!"
assert "pass" in j, "[ERROR] `pass` key does not exist!"
LOGIN = j["login"]
PASSWORD = j["pass"]
vk_session = vk_api.VkApi(
    login=LOGIN, password=PASSWORD, auth_handler=auth_handler)
vk_session.auth(token_only=True)

vk = vk_session.get_api()

try:
    response = vk.users.get(user_ids=args.screenName)
except:
    print("[ERROR] User {} does not exist!".format(args.screenName))
    exit(-1)
print(response[0]["id"])
