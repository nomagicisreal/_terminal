import subprocess
import os

print(
    '\n'
    '-----------------------------------------------\n'
    'yt-dlp.py helps downloading video by terminal.\n'
    "It's an implementation for https://github.com/yt-dlp/yt-dlp \n"
    "Supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md \n"
    '-----------------------------------------------\n'
)

embedThmbnail: str = '--embed-thumbnail'
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
# 
# args location
# 
# 
# 
def argsLocation() -> str:
    def availableDirs() -> str:
        return next(os.walk('.'))[1]
    
    path : str
    while (True):
        location = input(f'file location (default: {os.getcwd()}): ')

        args = location.split()
        argsLength = len(args)
        if argsLength == 0:
            path = outputFileNameFormat
            break
        
        if argsLength == 1:
            path = f'{args[0]}/{outputFileNameFormat}'
            break
        
        if argsLength == 2:
            command = args[0]
            location = args[1]

            if command == 'cd':
                try:
                    os.chdir(location)
                    print(f'availables dirs: {availableDirs()}')
                    continue
                except FileNotFoundError:
                    print(
                        f'directory not found: {location},\n'
                        f'availables: {availableDirs()}\n'
                    )
        
        print(
            f"unknown command: {args}\n"
            "USAGES:\n"
            "\t1. press enter to ensure the default location\n"
            "\t2. 'cd /your_path', pending to provide a location\n"
        )
    
    return [output, path]

# 
# 
# 
# args format
# 
# 
# 
def argsFormat(format: str) -> str:
    while (True):
        format = 'mp3' if format == '' else format

        if format in supportedAudioFormat:
            return [extractAudio, formatAudio, format]
        elif format in supportedVideoFormat:
            if format == 'mp4':
                format = f'bv*[ext={format}]+ba[ext=m4a]'
            else:
                raise Exception('currently only support mp4 for my implementation (not for yt-dlp)')
            
            # requireBestVideo = input('require best video (Y/N): ').capitalize()
            # if requireBestVideo == 'Y':
            #   format = f'bv*[ext={format}]+ba[ext=m4a]' # unimplement for N
            # if requireBestVideo == 'N':
            # 
            # else:
            #     print(f'except Y/y or N/n: {requireBestVideo}')
            #     continue
            return [formatVideo, format]
        
        print(
            f"unknown command: {format}\n"
            "USAGES:\n"
            f"\t1. press enter to ensure the default format\n"
            f"\t2. input an audio format of {supportedAudioFormat}\n"
            f"\t3. input a video format of {supportedVideoFormat}\n"
        )


# 
# 
# 
# 
# subprocess
# 
# 
# 
# 
url = input('url: ')

commands = ['yt-dlp']
commands.append(embedThmbnail)
commands.extend(argsLocation())

import sys
argv = sys.argv
commands.extend(
    argsFormat(
        format=input('file format (default: mp3): ') if len(argv) == 1 else argv[1]
    )
)

subprocess.call(commands + [url])

