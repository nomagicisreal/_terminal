from subprocess import call

# 
# 
# 
# constants
# 
# 
# 
argEnvironment = 'yt-dlp'
argEmbedThumbnail = '--embed-thumbnail'
argCookiesFromBrowser = '--cookies-from-browser'
argBrowserChrome = 'chrome'
argYesPlaylist = '--yes-playlist'
argOutput = '-o'
argOutputFileNameFormat = f'%(title)s'
argExtractAudio = '-x'
argFormatAudio = '--audio-format'
argFormatVideo = '-f'
mp4 = 'mp4'
mov = 'mov'
m4a = 'm4a'
mp3 = 'mp3'

# respectively according to https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#sorting-formats:~:text=Video%20Extension, https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#sorting-formats:~:text=Audio%20Extension
generalVideoExtension = [mp4, mov, 'webm']
generalAudioExtension = [m4a, 'aac', mp3, 'ogg', 'opus', 'webm']

# 
# 
# lambdas
# 
# 
downloading = lambda url, format: call([
    argEnvironment,
    argOutput, argOutputFileNameFormat,
    *argsPlatform(supportedUrl=url),
    *argsInputFormat(format=format),
    url
])

# 
# 
# 
# 
# 
# functions
# 
# 
# 
# 
# 
def argsPlatform(supportedUrl: str) -> list:
    # 
    # instagram needs to login before downloading
    # youtube has thumbnail, "youtu.be" occurs when copy url by sharing function
    # 
    if 'instagram' in supportedUrl: return [argCookiesFromBrowser, 'chrome']
    if 'youtube' in supportedUrl: return [argEmbedThumbnail]
    if 'youtu.be' in supportedUrl: return [argEmbedThumbnail]
    
    raise Exception(f'unsupported platform: {supportedUrl}')

def argsInputFormat(format: str) -> str:
    if format in generalVideoExtension:
        return [argFormatVideo, f'bv*[ext={format}]+ba[ext={m4a}]']
    if format in generalAudioExtension:
        return [argExtractAudio, argFormatAudio, format]
    
    raise Exception(f'unknown format: {format}')


# 
# 
# 
# functions --- readyTo...
# 
# 
# 
import script_input
def readyToDownload(format: str):
    format = script_input.inputOrDefaultIfEmpty('format', mp4, format)
    script_input.ensureLocation()
    downloading(script_input.ensureValidUrl(), format)

def readyToDownloadMany(format: str, askingLocationEverytime: bool):
    format = script_input.inputOrDefaultIfEmpty('format', mp4, format)
    if askingLocationEverytime:
        while True:
            script_input.ensureLocation()
            downloading(script_input.ensureValidUrl(), format)
            if not script_input.ensureYorN('continue downloading?', True): return
    
    script_input.ensureLocation()
    while True:
        downloading(script_input.ensureValidUrl(), format)
        if not script_input.ensureYorN('continue downloading?', True): return
    