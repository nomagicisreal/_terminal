import os

def availableDirs() -> str:
    return next(os.walk('.'))[1]

def availableFiles() -> str:
    return next(os.walk('.'))[2]

# 
# 
# 
# variables
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
# 
# args location
# 
# 
# 
def argsLocation() -> str:
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
