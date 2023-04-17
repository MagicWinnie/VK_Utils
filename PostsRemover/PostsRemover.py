"""
Delete posts older than date.
"""
import os
import calendar
from datetime import datetime, date, timezone
import json
from argparse import ArgumentParser
import vk_api
import pandas as pd


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


parser = ArgumentParser()
parser.add_argument(
    "user",
    type=str,
    help="User alias"
)
parser.add_argument(
    'date',
    type=date.fromisoformat,
    help="Input date as YYYY-MM-DD"
)
parser.add_argument(
    "--filter",
    type=str,
    default="all",
    help="What filters to use: owner, others, or all. See more at https://dev.vk.com/method/wall.get",
)
parser.add_argument(
    "--login",
    type=str,
    default="../LoginData/login.json",
    help="path to login.json (default: ../LoginData/login.json)",
)
args = parser.parse_args()
timestamp = int(datetime.combine(args.date, datetime.min.time()).replace(tzinfo=timezone.utc).timestamp())

assert args.filter in ('owner', 'others', 'all'), "Only following filters are allowed: owner, others, or all"
assert os.path.isfile(args.login), "[ERROR] {} is not a file or it does not exist!".format(args.login)

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

tools = vk_api.VkTools(vk_session)
vk = vk_session.get_api()

posts = tools.get_all_iter(
    'wall.get', 10,
    {
        "domain": args.user,
        "filter": args.filter
    }
)
print(f"[WARNING] This script will PERMANENTLY delete your posts that have been published earlier that {timestamp}. " + \
    "This is UNIX timestamp, please re-check the date. Input yes if you want to continue or anything else to stop.")
if input() != "yes":
    exit()
cnt = 0
for el in posts:
    post_id = el['id']
    owner_id = el['owner_id']
    post_timestamp = el['date']
    can_delete = el['can_delete']
    if post_timestamp < timestamp:
        res = vk.wall.delete(owner_id=owner_id, post_id=post_id)
        post_url = f"https://vk.com/{args.user}?w=wall{owner_id}_{post_id}"
        if not can_delete or not res:
            print(f"[WARNING] Cannot delete following post: {post_url}")
        else:
            cnt += 1
            print(f"[INFO] Deleted post: {post_url}")
print(f"[INFO] {cnt} posts have been removed")
