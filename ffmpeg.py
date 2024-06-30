import subprocess
import os
from ytdlp import availableFiles

# extract thumbnail from audio:
# ffmpeg -i audio.mp3 -an -c:v copy image.jpg

# add thumbnail to audio
# ffmpeg -i in.mp3 -i image.png -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" out.mp3

command = 'ffmpeg'
argInput = '-i'

def _transformThenDelete(argv: list):
    subprocess.call(argv)
    os.remove(argv[2])

def transformAll(extIn: str, extOut: str, removeTransformed: bool):
    # all = [files for files in availableFiles() if files.split('.')[1] == extIn]
    transform = _transformThenDelete if removeTransformed else lambda argv : subprocess.call(argv)
    for files in availableFiles():
        names = files.split('.')
        if names[1] == extIn:
            transform([
                command,
                argInput, files,
                f'{names[0]}.{extOut}'
            ])
