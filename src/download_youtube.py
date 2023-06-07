# Download youtube channel
# author : Michaël Launay
# date : 2023/05/14
# version : 0.0.1
# usage : python3 download_youtube.py

import os
import sys
import re
from pathlib import Path
import itertools
from collections import namedtuple
import argparse
#CMD_YOUTUBE_DL="snap run youtube-dl"
CMD_YOUTUBE_DL="/home/sav/Vidéos/youtube-dl/youtube-dl-master/bin/youtube-dl"
example = "python3 download_youtube.py --channel PasseScience --destination /home/sav/Vidéos/ --source /home/michaellaunay/tmp/20230514_passescience_videos.html --youtube-dl /home/sav/Vidéos/youtube-dl/youtube-dl-master/bin/youtube-dl"

parser = argparse.ArgumentParser(description="Download youtube channel", epilog=example)
parser.add_argument("--channel", dest="channel", help="Channel name", required=True)
parser.add_argument("--output", dest="destination", help="Destination directory", required=True)
parser.add_argument("--source", dest="source_file", help="File containing youtube page", required=True)
parser.add_argument("--youtube-dl", dest="youtube_dl_cmd", default=CMD_YOUTUBE_DL,help="Youtube-dl command", required=False)
parser.set_defaults(path=os.getcwd())
args = parser.parse_args()


existing_files = []
paths = Path(os.path.join(args.destination, args.channel)).glob("*.mp4")


#To retrieve a downloading we parse file in destination
mp4_reg = re.compile("[A-Za-z0-9]*_(?P<id>[A-Za-z0-9]*)_")
for p in paths:
    groups = mp4_reg.findall(p.name)
    if groups :
        id = groups[0]
        existing_files.append(id)

#cmd_line is used for exucting youtube dl
cmd_line = """cd "{destination}" && {youtube_dl_cmd} -f best -ciw -o "%(channel_id)s_%(id)s_%(title)s.%(ext)s" -v "https://www.youtube.com/watch?v={id}&ab_channel={channel}" """
#a_reg is a regular expression whith aim to extract video id
a_reg = re.compile('<a.*href="/watch\?v=(?P<id>[^"]*)"')
hrefs={}
Video = namedtuple("Video", ["id", "url"])
with open(args.source_file) as youtube_video_page :
    for line in youtube_video_page:
        matchs = a_reg.findall(line)
        if matchs:
            for id in matchs:
                if len(id) == 11:
                    hrefs[id] = Video(id, f"https://youtube.com/watch?v={id}&ab_channel={args.channel}")
                else:
                    print("Strange id {id} for line {line}", file=sys.stderr)

#Check if video is allready downloaded with id
print(f"Ids to download = {hrefs.keys()}")
for id in hrefs:
    if id in existing_files:
        print(f"{id} already downloaded, pass", sys.stderr)
        continue
    cmd = cmd_line.format(destination=args.destination, youtube_dl_cmd=args.youtube_dl_cmd, id=id, channel=args.channel)
    res = os.system(cmd)
    if res==0:
        print(f"{id} downloaded with success", sys.stderr)
    else:
        print(f"{id} failed ! {cmd}: {res}", sys.stderr)



