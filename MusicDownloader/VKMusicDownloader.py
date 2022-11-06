"""
Downloads music from VK
By @MagicWinnie
"""

import os
import json
from argparse import ArgumentParser

# working with mp3
import mutagen
import music_tag
import streamlink
import ffmpeg
from io import BytesIO

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
vk_session = vk_api.VkApi(  # type: ignore
    login=login,
    password=password,
    auth_handler=auth_handler,
    captcha_handler=captcha_handler,
)
vk_session.auth(token_only=True)

vk = vk_session.get_api()
vk_audio = audio.VkAudio(vk_session)

FINAL_PATH = os.path.join(SAVE_PATH, str(user_id))

if not (os.path.exists(FINAL_PATH)):
    os.mkdir(FINAL_PATH)

# get audio list
print("[INFO] Getting audio file urls.")
audios = vk_audio.get(owner_id=user_id)
print("{l} audio files will be downloaded to {p}".format(
    l=len(audios), p=FINAL_PATH))

failed = []

print("[INFO] Starting downloading.")
for ind, aud in enumerate(audios):
    fileName = "{artist} - {title}.mp3".format(
        artist=aud["artist"], title=aud["title"]
    )
    fileName = remove_symbols(fileName)
    fileName = os.path.join(FINAL_PATH, fileName)
    try:
        if os.path.isfile(fileName):
            print("{} - Is already downloaded: {}".format(ind + 1, fileName))
        else:
            print("{} - Downloading: {}".format(ind + 1, fileName), end=" - ", flush=True)
            streams = streamlink.streams(audios[ind]["url"])
            fd = streams["best"].open()
            byt = BytesIO()
            while True:
                data = fd.read(2**20)
                byt.write(data)
                if not data:
                    break
            fd.close()
            byt.seek(0)
            process = ffmpeg.input("pipe:").output(fileName).run_async(quiet=True, pipe_stdin=True)
            process.communicate(input=byt.getbuffer())
            print("Done.")
    except FileNotFoundError:
        print("\n[ERROR] You do not have FFMPEG or it's path is not in system variables.")
        quit()

    # fix metadata && check if corrupted
    try:
        m = music_tag.load_file(fileName)
        del m["album"]  # type: ignore
        del m["tracknumber"]  # type: ignore
        del m["genre"]  # type: ignore
        m["artist"] = aud["artist"]  # type: ignore
        m["title"] = aud["title"]  # type: ignore
        m.save()  # type: ignore
    except mutagen.mp3.HeaderNotFoundError:  # type: ignore
        print(
            "{} - Failed to download (HeaderNotFoundError): {}".format(
                ind + 1, fileName
            )
        )
        failed.append(fileName)
    except PermissionError:
        print(
            "{} - Failed to download (PermissionError). Re-run the app: {}".format(
                ind + 1, fileName
            )
        )
        failed.append(fileName)


# remove failed downloads
if len(failed) > 0:
    print("\n[WARNING] Failed to download {} files:".format(len(failed)))
    for num, aud in enumerate(failed):
        print("{}. {}".format(num + 1, aud))
        os.remove(os.path.join(FINAL_PATH, aud))
else:
    print("\n[INFO] No failed downloads")
print("[INFO] Done.")
