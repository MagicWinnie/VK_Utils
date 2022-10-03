"""
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
"""

import os
import json
import requests
from argparse import ArgumentParser

# working with mp3
import mutagen
import music_tag

# working with vk api
import vk_api
from vk_api import audio


def auth_handler(remember_device: bool = True):
    key = input("Enter authentication code: ")
    return key, remember_device


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def remove_symbols(s: str) -> str:
    blacklist = {"/": "_", "?": "", "!": "", "|": "", '"': "'"}

    s = s.strip()
    for i in blacklist:
        s = s.replace(i, blacklist[i])

    return s


parser = ArgumentParser()
parser.add_argument("output", type=str, help="Output path")
parser.add_argument("userID", type=int, help="User ID")
parser.add_argument(
    "--login",
    type=str,
    default="../LoginData/login.json",
    help="path to login.json (default: ../LoginData/login.json)",
)
args = parser.parse_args()

SAVE_PATH = args.output

if not (os.path.exists(SAVE_PATH)):
    os.mkdir(SAVE_PATH)

# load credentials
assert os.path.isfile(
    args.login), "[ERROR] {} is not a file or it does not exist!".format(args.login)
j = json.load(open(args.login, "r"))

assert "login" in j, "[ERROR] `login` key does not exist!"
assert "pass" in j, "[ERROR] `pass` key does not exist!"
login = j["login"]
password = j["pass"]
user_id = args.userID

# auth in vk
vk_session = vk_api.VkApi(
    login=login,
    password=password,
    auth_handler=auth_handler,
    captcha_handler=captcha_handler,
)
vk_session.auth()

vk = vk_session.get_api()
vk_audio = audio.VkAudio(vk_session)

FINAL_PATH = os.path.join(SAVE_PATH, str(user_id))

if not (os.path.exists(FINAL_PATH)):
    os.mkdir(FINAL_PATH)

# get audio list
audios = vk_audio.get(owner_id=user_id)
print("{l} audio files will be downloaded to {p}".format(
    l=len(audios), p=FINAL_PATH))

failed = []

for ind, i in enumerate(audios):
    fileFormat = "{artist} - {title}.mp3".format(
        artist=i["artist"], title=i["title"])
    fileFormat = remove_symbols(fileFormat)

    try:
        if os.path.isfile(os.path.join(FINAL_PATH, fileFormat)):
            print("{} - Is already downloaded: {}".format(ind + 1, fileFormat))
        else:
            print("{} - Downloading: {}".format(ind + 1, fileFormat), end=" - ")
            r = requests.get(audios[ind]["url"])
            if r.status_code == 200:
                print("Finished")
                with open(os.path.join(FINAL_PATH, fileFormat), "wb") as out:
                    out.write(r.content)
    except OSError:
        print("{} - Failed to download (OSError): {}".format(ind + 1, fileFormat))
        failed.append(fileFormat)

    # fix metadata && check if corrupted
    try:
        m = music_tag.load_file(os.path.join(FINAL_PATH, fileFormat))
        del m["album"]
        del m["tracknumber"]
        del m["genre"]
        m["artist"] = i["artist"]  # f.split(' - ')[0]
        m["title"] = i["title"]  # f.split(' - ')[1][:-4]
        m.save()
    except mutagen.mp3.HeaderNotFoundError:
        print(
            "{} - Failed to download (HeaderNotFoundError): {}".format(
                ind + 1, fileFormat
            )
        )
        failed.append(fileFormat)
    except PermissionError:
        print(
            "{} - Failed to download (PermissionError). Re-run the app: {}".format(
                ind + 1, fileFormat
            )
        )
        failed.append(fileFormat)


# remove failed downloads
if len(failed) > 0:
    print("\nFailed to download {} files:".format(len(failed)))
    for num, i in enumerate(failed):
        print("{}. {}".format(num + 1, i))
        os.remove(os.path.join(FINAL_PATH, i))
else:
    print("\nNo failed downloads")
