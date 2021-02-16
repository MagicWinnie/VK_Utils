'''
Getting peoples' birthday into a table
By @MagicWinnie
'''

import pandas as pd
import vk_api
from vk_messages import MessagesAPI

def auth_handler():
    return input("Enter authentication code: "), True

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

LOGIN = ''
PASSWORD = ''

vk_session = vk_api.VkApi(
    LOGIN, PASSWORD,
    auth_handler=auth_handler,
    captcha_handler=captcha_handler
)

messages = MessagesAPI(login=LOGIN, password=PASSWORD,
                two_factor=True, cookies_save_path='sessions/')

try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)
    quit(-1)

vk = vk_session.get_api()

d = dict(messages.method('messages.getChat', chat_id=126))

print(d['users'])

users_info = vk.users.get(user_ids=d['users'], fields='bdate')
ids = [x['id'] for x in users_info]
first_names = [x['first_name'] for x in users_info]
last_names = [x['last_name'] for x in users_info]
bdates = []

for x in users_info:
    try:
        bdates.append(x['bdate'])
    except:
        bdates.append(None)

df_dict = {'id': ids, 'first_name': first_names, 'last_name': last_names, 'bdate': bdates}
df = pd.DataFrame(df_dict)

df.to_csv('birthdays.csv', index=False)
