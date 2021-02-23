'''
Downloads music from VK
* Create a `json` file with login, password and user id:
`json` file format: 
{
    'login': '',
    'pass': '',
    'user_id': 
}

* Put the `json` file next to the script
By @MagicWinnie
'''

import os
import sys
import json
import getopt
import pickle
import requests
from time import time
import vk_api
from vk_api import audio
import re

def auth_handler(remember_device: bool=True)->(str, bool):
    key = input("Enter authentication code: ")
    return key, remember_device

def remove_symbols(s: str)->str:
    blacklist = {
        '/': '_',
        '?': '',
        '!': '',
        '|': '',
        '"': "'"
    }
    
    s = s.strip()

    for i in blacklist:
        s = s.replace(i, blacklist[i])
    
    return s

SAVE_PATH = ""

if not(os.path.exists(SAVE_PATH)):
    os.mkdir(SAVE_PATH)
    
import platform
if platform.system() == "Windows":
    FOLDER = '\\'.join(os.path.realpath(__file__).split('\\')[:-1])
else:
    FOLDER = '/'.join(os.path.realpath(__file__).split('/')[:-1])

j = json.load(open(os.path.join(FOLDER, 'login.json'), 'r'))

login = j['login']
password = j['pass']
user_id = j['user_id']

vk_session = vk_api.VkApi(login=login, password=password, auth_handler=auth_handler)
vk_session.auth()

vk = vk_session.get_api()
vk_audio = audio.VkAudio(vk_session)

FINAL_PATH = os.path.join(SAVE_PATH, str(user_id))

if not(os.path.exists(FINAL_PATH)):
    os.mkdir(FINAL_PATH)

audio = vk_audio.get(owner_id=user_id)
print("{l} audio files will be downloaded to {p}".format(l=len(audio), p=FINAL_PATH))

failed = []

for ind, i in enumerate(audio):
    fileFormat = "{artist} - {title}.mp3".format(artist=i['artist'], title=i['title'])
    fileFormat = remove_symbols(fileFormat)

    try:
        if os.path.isfile(os.path.join(FINAL_PATH, fileFormat)):
            print("{} - Is already downloaded: {}".format(ind + 1, fileFormat))
        else :
            print("{} - Downloading: {}".format(ind + 1, fileFormat), end = " - ")
            r = requests.get(audio[ind]["url"])
            if r.status_code == 200:
                print("Finished")
                with open(os.path.join(FINAL_PATH, fileFormat), 'wb') as out:
                    out.write(r.content)
    except OSError:
        print("{} - Failed to download: {}".format(ind + 1, fileFormat))
        failed.append(fileFormat)

if len(failed) > 0:
    print("\nFailed to download {} files".format(len(failed)))
    for i in failed:
        print(i)
else:
    print("\nNo failed downloads")
