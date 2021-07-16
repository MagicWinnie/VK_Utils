"""
Using: https://habr.com/ru/sandbox/146880/
"""
import os
import ast
import json
import random
import requests
from argparse import ArgumentParser
from pydub import AudioSegment
from vk_messages import MessagesAPI



parser = ArgumentParser()
parser.add_argument("file", type=str, help="Your audio file")
parser.add_argument("peerID", type=int, help="User ID of the person you are sending to")
parser.add_argument(
    "--login",
    type=str,
    default="../LoginData/login.json",
    help="path to login.json (default: ../LoginData/login.json)",
)
parser.add_argument(
    "--message",
    type=str,
    default="",
    help="Message text",
)
args = parser.parse_args()



assert os.path.isfile(
    args.login
), "[ERROR] {} is not a file or it does not exist!".format(args.login)
with open(args.login, "r") as f:
    j = json.load(f)

assert "login" in j, "[ERROR] `login` key does not exist!"
assert "pass" in j, "[ERROR] `pass` key does not exist!"
assert "access_token" in j, "[ERROR] `access_token` key does not exist! Get one at https://oauth.vk.com/authorize?client_id=3116505&scope=1073737727&response_type=token&revoke=1"
LOGIN = j["login"]
PASSWORD = j["pass"]
ACCESS_TOKEN = j["access_token"]
messages = MessagesAPI(login=LOGIN, password=PASSWORD, two_factor=True)



print("[INFO] Converting the file...")
assert os.path.isfile(
    args.file
), "[ERROR] {} is not a file or it does not exist!".format(args.file)
SUPPORTED_IN_FORMATS = ["mp3", "ogg", "wav", "aac", "mp4", "flv"]
assert (
    args.file.split(".")[-1] in SUPPORTED_IN_FORMATS
), "[ERROR] {} is not supported! Only supported: {}".format(
    args.file, ", ".join(SUPPORTED_IN_FORMATS)
)
sound = AudioSegment.from_file(args.file)
sound.export(args.file.split(".")[0] + ".ogg", format="ogg")
print("[INFO] Converted the file...")





print("[INFO] Getting upload server...")
getUploadServer = "https://api.vk.com/method/docs.getUploadServer?access_token={}&type=audio_message&v=5.63".format(ACCESS_TOKEN)
response = requests.post(getUploadServer)
raw = ast.literal_eval(response.content.decode("utf-8"))
if "error" in raw:
    print("[ERROR] Error while getting upload url. Response:")
    print(raw)
    exit(-1)
upload_url = raw["response"]["upload_url"].replace("\/", "/")
print("[INFO] Got upload server...")





print("[INFO] Getting file data...")
response = requests.post(
    upload_url, files={"file": open(args.file.split(".")[0] + ".ogg", "rb")}
)
raw = response.content.decode("utf-8")
if "error" in raw:
    print("[ERROR] Error while getting file data. Response:")
    print(raw)
    exit(-1)
processed = ast.literal_eval(raw)["file"]
print("[INFO] Got file data...")





print("[INFO] Saving the file...")
processed = messages.method("docs.save", file=processed)
if "error" in processed:
    print("[ERROR] Error while saving the file. Response:")
    print(raw)
    exit(-1)

MEDIA_ID = processed["audio_message"]["id"]
OWNER_ID = processed["audio_message"]["owner_id"]
ATTACHMENT = "doc{}_{}".format(OWNER_ID, MEDIA_ID)
response = messages.method("messages.send", random_id=random.randint(0, 2147483647), peer_id=args.peerID, message=args.message, attachment=ATTACHMENT)
if "error" in raw:
    print("[ERROR] Error while sending the audio. Response:")
    print(raw)
    exit(-1)

print("[INFO] Done")