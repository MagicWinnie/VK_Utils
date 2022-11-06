"""
Using: https://habr.com/ru/sandbox/146880/
"""
import os
import ast
import json
import requests
from argparse import ArgumentParser
from pydub import AudioSegment
import vk_api


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


parser = ArgumentParser()
parser.add_argument(
    "file",
    type=str,
    help="Your audio file"
)
parser.add_argument(
    "--login",
    type=str,
    default="../LoginData/login.json",
    help="path to login.json (default: ../LoginData/login.json)",
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

vk_session = vk_api.VkApi(
    login=LOGIN, password=PASSWORD,
    auth_handler=auth_handler
)
vk_session.auth(token_only=True)
vk = vk_session.get_api()

print("[INFO] Converting the file...")
assert os.path.isfile(args.file),\
    "[ERROR] {} is not a file or it does not exist!".format(args.file)
SUPPORTED_IN_FORMATS = ("mp3", "ogg", "wav", "aac", "mp4", "flv")
assert (args.file.split(".")[-1] in SUPPORTED_IN_FORMATS),\
    "[ERROR] {} is not supported! Only supported: {}".format(
        args.file, ", ".join(SUPPORTED_IN_FORMATS)
)
sound = AudioSegment.from_file(args.file)
sound.export(args.file.split(".")[0] + ".ogg", format="ogg")
print("[INFO] Converted the file...")

print("[INFO] Getting upload server...")
upload_url = vk.docs.getMessagesUploadServer(
    type="audio_message")["upload_url"]
print("[INFO] Got upload server...")

print("[INFO] Getting file data...")
response = requests.post(
    upload_url,
    files={
        "file": open(args.file.split(".")[0] + ".ogg", "rb")
    }
)
raw = response.content.decode("utf-8")
if "error" in raw:
    print("[ERROR] Error while getting file data. Response:")
    print(raw)
    exit(-1)
processed = ast.literal_eval(raw)["file"]
print("[INFO] Got file data...")

print("[INFO] Saving the file...")
processed = vk.docs.save(file=processed)
if "error" in processed:
    print("[ERROR] Error while saving the file. Response:")
    print(raw)
    exit(-1)

MEDIA_ID = processed["audio_message"]["id"]
OWNER_ID = processed["audio_message"]["owner_id"]
ATTACHMENT = "vk.com/doc{}_{}".format(OWNER_ID, MEDIA_ID)
print("Send this url to person:", ATTACHMENT)
print("[INFO] Done")
