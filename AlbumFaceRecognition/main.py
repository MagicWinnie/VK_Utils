import os
import glob

import json
import pickle


import vk_api
import urllib.error

import numpy as np
import skimage
import face_recognition

from tqdm import tqdm
from config import *


def auth_handler():
    '''
    2FA handler for VK api
    '''
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


img_urls = []
if not RESTORE_PHOTOS_FROM_PICKLE:
    # login to vk
    assert os.path.isfile(LOGIN_DATA_PATH),\
        "[ERROR] {} is not a file or it does not exist!".format(LOGIN_DATA_PATH)
    with open(LOGIN_DATA_PATH, "r") as f:
        j = json.load(f)
    LOGIN = j["login"]
    PASSWORD = j["pass"]
    vk_session = vk_api.VkApi(
        login=LOGIN,
        password=PASSWORD,
        auth_handler=auth_handler
    )
    vk_session.auth(token_only=True)
    tools = vk_api.VkTools(vk_session)
    vk = vk_session.get_api()

    # get photo urls
    albums_dict = vk.photos.getAlbums(
        owner_id=OWNER_ID,
        album_ids=ALBUM_IDS
    )
    albums = albums_dict['items']
    print('[INFO] Getting images from albums.')
    for album in tqdm(albums):
        if album['created'] < OLDEST_ALBUM_UNIX_TIME:
            continue
        photos = vk.photos.get(
            owner_id=album['owner_id'],
            album_id=album['id'],
            photo_sizes='1'
        )
        for photo in photos['items']:
            img_url = ''
            for size in photo['sizes']:
                if size['type'] == IMAGE_SIZE_TYPE:
                    img_url = size['url']
                    break
            else:
                tqdm.write("[WARNING] Not found needed image size.")
                continue
            img_urls.append((img_url, album['id'], photo['id']))
    with open(LIST_PHOTOS_PICKLE_FILENAME, 'wb') as pkl_out_file:
        pickle.dump(img_urls, pkl_out_file)
else:
    with open(LIST_PHOTOS_PICKLE_FILENAME, 'rb') as pkl_inp_file:
        img_urls = pickle.load(pkl_inp_file)

# get known faces
known_faces = []
known_faces_filenames = []
print("[INFO] Loading known face data...")
for f in tqdm(glob.glob("known_people/*.jpg")):
    img = face_recognition.load_image_file(f)
    img_encodings = face_recognition.face_encodings(img, model=MODEL)
    if len(img_encodings) == 0:
        tqdm.write(f"[WARNING] No faces were found in {f}.")
        continue
    elif len(img_encodings) > 1:
        tqdm.write(
            f"[WARNING] Image {f} contains more than one person. Choosing random.")
    known_faces.append(img_encodings[0])
    known_faces_filenames.append(f)
if len(known_faces) == 0:
    print("[ERROR] No faces were found. Check the images.")
    quit()

# process faces
for j in tqdm(range(IMG_URLS_OFFSET, len(img_urls))):
    img_url = img_urls[j][0]
    image = np.array([])
    for attempt in range(NUMBER_OF_ATTEMPTS):
        try:
            image = skimage.io.imread(img_url)
        except urllib.error.URLError:
            tqdm.write(f"[ERROR] Unable to open {img_url}.", end=' ')
            tqdm.write(f"Attempt #{attempt + 1}/{NUMBER_OF_ATTEMPTS}.")
        except KeyboardInterrupt:
            print(f"[INFO] Keyboard Interrupt.")
            quit()
        else:
            break
    if not image.size:
        tqdm.write(f"[ERROR] Could not open {img_url}. Check internet connection.")
        continue
    image_encodings = face_recognition.face_encodings(image, model=MODEL)
    if len(image_encodings) == 0 and not SUPPRESS_NOT_FOUND_IN_ALBUMS:
        tqdm.write(f"[WARNING] No faces were found. URL: {img_url}.")
        continue
    for img_enc in image_encodings:
        results = face_recognition.compare_faces(
            known_faces,
            img_enc,
            tolerance=TOLERANCE
        )
        for i in range(len(results)):
            if results[i]:
                tqdm.write(f"[INFO] Found {known_faces_filenames[i]}.", end=' ')
                tqdm.write(f"Album ID: {img_urls[j][1]}", end=' ')
                tqdm.write(f"Photo ID: {img_urls[j][2]}", end=' ')
                tqdm.write(f"URL: {img_url}")
print(f"[INFO] Done.")
