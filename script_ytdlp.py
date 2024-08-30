from script import raiseUnimplementUsecase
from script import askForLocation, askForLocationInstruction, chooseDirectoryOn

# 
# 
# 
# constants
# 
# 
# 
argEnvironment = 'yt-dlp'
argEmbedThumbnail: str = '--embed-thumbnail'
argYesPlaylist: str = '--yes-playlist'

argOutput: str = '-o'
argOutputFileNameFormat: str = f'%(title)s'

# see also https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#format-selection-examples
argExtractAudio: str = '-x'
argFormatAudio: str = '--audio-format'
argFormatVideo: str = '-f'
argSupportedAudioFormat = ['best', 'aac', 'alac', 'flac', 'm4a', 'mp3', 'opus', 'vorbis', 'wav'] # see also https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#post-processing-options
argSupportedVideoFormat = ['avi', 'flv', 'mkv', 'mov', 'mp4', 'webm'] # see also https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#video-format-options

# 
# 
# thumbnail
# 
#   - instagram: x
#   - youtube: o
# 
def requireThumbnailIf(supportedUrl: str) -> list:
    if 'instagram' in supportedUrl:
        return []
    else:
        return [argEmbedThumbnail]



# 
# 
# 
# require location
# 
# 
# 
def whileInputLocation() -> str:
    while True:
        destination = askForLocation()

        args = destination.split()
        argsLength = len(args)
        if argsLength == 0:
            return [argOutput, argOutputFileNameFormat]
        
        if argsLength == 1:
            return [argOutput, f'{args[0]}/{argOutputFileNameFormat}']
        
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
def whileInputFormat(defaultOption: str) -> str:
    format = checkInputFormatFrom(defaultOption)
    while True:
        if format in argSupportedAudioFormat:
            return [argExtractAudio, argFormatAudio, format]
        elif format in argSupportedVideoFormat:
            if format == 'mp4':
                format = f'bv*[ext={format}]+ba[ext=m4a]'
            else:
                raise Exception('currently only support mp4 with my implementation')
            return [argFormatVideo, format]
        
        print(
            f"unknown command: {format}\n"
            "USAGES:\n"
            f"\t1. press enter to ensure the default format\n"
            f"\t2. input an audio format of {argSupportedAudioFormat}\n"
            f"\t3. input a video format of {argSupportedVideoFormat}\n"
        )

def checkInputFormatFrom(defaultOption: str):
    from script_api import usecaseDowloadVideoOrAudio, usecaseDowloadMp3, usecaseDowloadMp4
    if defaultOption == usecaseDowloadVideoOrAudio: return input('format (default: mp3): ')
    elif defaultOption == usecaseDowloadMp3: return 'mp3'
    elif defaultOption == usecaseDowloadMp4: return 'mp4'
    
    raiseUnimplementUsecase(argEnvironment, defaultOption)