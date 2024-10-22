from script import raiseUnimplementUsecase, whileEnsureFileLocation

# 
# 
# 
# constants
# 
# 
# 
argEnvironment = 'yt-dlp'
argEmbedThumbnail: str = '--embed-thumbnail'
argCookiesFromBrowser: str = '--cookies-from-browser'
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
def argsForPlatform(supportedUrl: str) -> list:
    if 'instagram' in supportedUrl:
        # return []
        return [argCookiesFromBrowser, 'chrome']
    else:
        return [argEmbedThumbnail]

def argsForLocation(asking: bool) -> list:
    if asking: whileEnsureFileLocation()
    return [argOutput, argOutputFileNameFormat]

# 
# 
# 
# args format
# 
# 
# 
def argsForInputFormat(defaultUsecase: str) -> str:
    format = checkInputFormatFrom(defaultUsecase)
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

def checkInputFormatFrom(defaultUsecase: str):
    from script_api import usecaseDowloadVideoOrAudio, usecaseDowloadMp3, usecaseDowloadMp4
    from script_api import usecaseDowloadMultipleMp3, usecaseDowloadMultipleMp3OnCwd
    if defaultUsecase == usecaseDowloadVideoOrAudio: return input('format (default: mp3): ')
    elif defaultUsecase == usecaseDowloadMp3: return 'mp3'
    elif defaultUsecase == usecaseDowloadMp4: return 'mp4'
    elif defaultUsecase == usecaseDowloadMultipleMp3: return 'mp3'
    elif defaultUsecase == usecaseDowloadMultipleMp3OnCwd: return 'mp3'
    
    raiseUnimplementUsecase(argEnvironment, defaultUsecase)