"""
Get people who liked post
"""
import os
import re
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
    "url",
    type=str,
    help="Url to vk post"
)
parser.add_argument(
    "output",
    type=str,
    help="Path to the output .csv file"
)
parser.add_argument(
    "--login",
    type=str,
    default="../LoginData/login.json",
    help="path to login.json (default: ../LoginData/login.json)",
)
args = parser.parse_args()

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
    login=LOGIN, password=PASSWORD,
    auth_handler=auth_handler
)
vk_session.auth(token_only=True)

tools = vk_api.VkTools(vk_session)
vk = vk_session.get_api()

# choose object type
# implemented: post, comment, photo, video
# full list: https://dev.vk.com/method/likes.getList
CHECK_IF_VK = re.compile(
    r'^(http:\/\/|https:\/\/)?(www.)?(vk\.com|vkontakte\.ru)'
)
CHECK_IF_IMPLEMENTED = re.compile(
    r'((?<=\/|=)wall|photo|video)(-?[0-9]*)_([0-9]*)(\?reply=)?((?<=reply=)[0-9]*)?'
)

vk_url = CHECK_IF_IMPLEMENTED.search(args.url)
assert CHECK_IF_VK.search(args.url), "You have not entered a VK url"
assert vk_url, "You have not entered wall/comment/photo/video url"

vk_type = vk_url.group(1)
vk_owner_id = vk_url.group(2)
vk_item_id = vk_url.group(3)
vk_reply_id = vk_url.group(5)

TYPE = ''
if vk_type == 'wall' and not vk_reply_id:
    TYPE = 'post'
    OWNER_ID = vk_owner_id
    ITEM_ID = vk_item_id
elif vk_type == 'photo':
    TYPE = 'photo'
    OWNER_ID = vk_owner_id
    ITEM_ID = vk_item_id
elif vk_type == 'video':
    TYPE = 'video'
    OWNER_ID = vk_owner_id
    ITEM_ID = vk_item_id
elif vk_type == 'wall' and vk_reply_id:
    TYPE = 'comment'
    OWNER_ID = vk_owner_id
    ITEM_ID = vk_reply_id
else:
    raise Exception('Unknown VK object type')

likes = tools.get_all(
    'likes.getList', 1000,
    {
        'type': TYPE,
        'filter': 'likes',
        'owner_id': OWNER_ID,
        'item_id': ITEM_ID,
    }
)['items']
# List of all available fields:
# https://dev.vk.com/method/users.get
# https://dev.vk.com/reference/objects/user
FIELDS = 'bdate,city,education,sex,relation,schools,universities'
row_list = []
for i in range(0, len(likes), 100):
    response = vk.users.get(
        user_ids=','.join(list(map(str, likes[i: i + 100]))),
        fields=FIELDS
    )
    for r in response:
        row_list.append(
            {
                'id': r['id'],
                'first_name': r['first_name'],
                'last_name': r['last_name'],
                'bday': r['bdate'].split('.')[0] if 'bdate' in r else '',
                'bmonth': r['bdate'].split('.')[1] if 'bdate' in r else '',
                'byear': r['bdate'].split('.')[2] if 'bdate' in r and len(r['bdate'].split('.')) == 3 else '',
                'city': r['city']['title'] if 'city' in r else '',
                'sex': r['sex'],
                'relation': r['relation'] if 'relation' in r else '',
                'last_school': r['schools'][-1]['name'] if 'schools' in r and r['schools'] else '',
                'last_university': r['universities'][-1]['name'] if 'universities' in r and r['universities'] else '',
            }
        )
df = pd.DataFrame(row_list, columns=['id', 'first_name', 'last_name', 'bday',
                  'bmonth', 'byear', 'city', 'sex', 'relation', 'last_school', 'last_university'])
df.to_csv(args.output, sep=',', index=False)
