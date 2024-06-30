import os
from ffmpeg import *
from api import yesOrNo

print(
    '\n'
    '-----------------------------------------------\n'
    'ffmpeg.py helps transform video or audio by terminal.\n'
    "It's an implementation for https://ffmpeg.org/ \n"
    '-----------------------------------------------\n'
)

print(f'\nlocation: {os.getcwd()}')
inputFormat = input('input format (default: mp4): ')
outputFormat = input('output format (default: mov): ')
removeTransformed = yesOrNo('remove transformed? ')
transformAll(
    'mp4' if inputFormat == '' else inputFormat,
    'mov' if outputFormat == '' else outputFormat,
    removeTransformed
)