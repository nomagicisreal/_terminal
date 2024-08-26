from script_api import *

# 
# 
# 
# constants
# 
# 
# 
embedThumbnail: str = '--embed-thumbnail'
yesPlaylist: str = '--yes-playlist'

output: str = '-o'
outputFileNameFormat: str = f'%(title)s'

# see also https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#format-selection-examples
extractAudio: str = '-x'
formatAudio: str = '--audio-format'
formatVideo: str = '-f'
supportedAudioFormat = ['best', 'aac', 'alac', 'flac', 'm4a', 'mp3', 'opus', 'vorbis', 'wav'] # see also https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#post-processing-options
supportedVideoFormat = ['avi', 'flv', 'mkv', 'mov', 'mp4', 'webm'] # see also https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#video-format-options

# 
# 
# url
# 
# 
def requireUrl() -> str:
    url: str = ''
    while url == '':
        url = input('url: ')
    return url

# 
# 
# thumbnail
# 
#   - instagram: x
#   - youtube: o
# 
def requireThumbnailFor(url: str) -> list:
    if 'instagram' in url:
        return []
    else:
        return [embedThumbnail]



# 
# 
# 
# require location
# 
# 
# 
def requireLocation() -> str:
    while True:
        destination = askForLocation()

        args = destination.split()
        argsLength = len(args)
        if argsLength == 0:
            return outputFileNameFormat
        
        if argsLength == 1:
            return f'{args[0]}/{outputFileNameFormat}'
        
        if argsLength == 2:
            command = args[0]
            if command == 'cd':
                chooseDirectoryOn(args[1])
                continue
        
        askForLocationInstruction(args)
    

# 
# 
# 
# args format
# 
# 
# 
def getInputFormatFrom(option: str):
    if option == optionDowloadVideoOrAudio:
        return input('file format (default: mp3): ')
    elif option == optionDowloadMp3:
        return 'mp3'
    elif option == optionDowloadMp4:
        return 'mp4'
    
    raiseUnimplementOption(__file__, option)

def requireFormat(format: str) -> str:
    while (True):
        if format in supportedAudioFormat:
            return [extractAudio, formatAudio, format]
        elif format in supportedVideoFormat:
            if format == 'mp4':
                format = f'bv*[ext={format}]+ba[ext=m4a]'
            else:
                raise Exception('currently only support mp4 with my implementation')
            return [formatVideo, format]
        
        print(
            f"unknown command: {format}\n"
            "USAGES:\n"
            f"\t1. press enter to ensure the default format\n"
            f"\t2. input an audio format of {supportedAudioFormat}\n"
            f"\t3. input a video format of {supportedVideoFormat}\n"
        )