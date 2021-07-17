"""
Get user ID
"""
import os
import json
from argparse import ArgumentParser
from vk_messages import MessagesAPI
import vk_messages


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

assert os.path.isfile(
    args.login
), "[ERROR] {} is not a file or it does not exist!".format(args.login)
with open(args.login, "r") as f:
    j = json.load(f)

assert "login" in j, "[ERROR] `login` key does not exist!"
assert "pass" in j, "[ERROR] `pass` key does not exist!"
LOGIN = j["login"]
PASSWORD = j["pass"]
messages = MessagesAPI(login=LOGIN, password=PASSWORD, two_factor=True)

try:
    response = messages.method("users.get", user_ids=args.screenName)
except vk_messages.vk_messages.Exception_MessagesAPI:
    print("[ERROR] User {} does not exist!".format(args.screenName))
    exit(-1)
print(response[0]["id"])
