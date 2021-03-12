import os
import sys
import mutagen
import music_tag

if len(sys.argv) != 2:
    print("Usage: python3 MusicMetadataFix.py <SavePath>")
    exit(-1)
else:
    MUSIC = sys.argv[1]

FILES = list(filter(lambda x: x.split('.')[-1].lower() == 'mp3', os.listdir(MUSIC)))
CORRUPT = []

for f in FILES:
    try:
        m = music_tag.load_file(os.path.join(MUSIC, f))
        del m['album']
        del m['tracknumber']
        m['artist'] = f.split(' - ')[0]
        m['title'] = f.split(' - ')[1][:-4]
        m.save()
    except mutagen.mp3.HeaderNotFoundError:
        print(f, '- Corrupted!!!')
        CORRUPT.append(f)
    else:
        print(f, '- Finished')

if len(CORRUPT) == 0:
    print("No corrupted files")
else:
    print("Corrupted: {}".format(CORRUPT))
