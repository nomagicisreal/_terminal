import sys
option = sys.argv[1]
import subprocess
from ytdlp import *

print(
    '\n'
    '-----------------------------------------------\n'
    'ytdlp.py helps downloading video by terminal.\n'
    "It's an implementation for https://github.com/yt-dlp/yt-dlp \n"
    "Supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md \n"
    '-----------------------------------------------\n'
)

url: str = ''
while url == '':
    url = input('url: ')

commands = ['yt-dlp']

# commands.append(embedThumbnail) # error on instagram post for youtube

# for domain in enumerate(url.split('.')):
#     if domain == 'youtube':
#         commands.append(embedThumbnail)
#         break

commands.extend(argsLocation())
inputFormat = input('file format (default: mp3): ') if option == '' else option
commands.extend(
    argsFormat('mp3' if inputFormat == '' else inputFormat)
)
subprocess.call(commands + [url])