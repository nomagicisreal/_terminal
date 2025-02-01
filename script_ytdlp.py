# 
# 
# -----------------------------------------------
# yt-dlp.py helps to download video by terminal.
# Implementation for https://github.com/yt-dlp/yt-dlp 
# Supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md 
# -----------------------------------------------
# 
# 

# 
# 
# 
# constants
# 
# 
# 
argEnvironment = 'yt-dlp'
argGetTitle = '--get-title'
argEmbedThumbnail = '--embed-thumbnail'
argCookiesFromBrowser = '--cookies-from-browser'
argBrowserChrome = 'chrome'
argYesPlaylist = '--yes-playlist'
argOutputFormat = '-o'
argExtractAudio = '-x'
argFormatAudio = '--audio-format'
argFormatVideo = '-f'

# see available fields https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#output-template-examples:~:text=processing%20is%20complete.-,The%20available%20fields%20are
formatTitle = f'%(title)s'
formatId = f'%(id)s'

# 
# 
# 
# 
# lambdas
# 
# 
# 
# 

import subprocess
download = lambda url, ext, format = formatTitle, check = False: subprocess.run([
    argEnvironment,
    argOutputFormat, format,
    *argsPlatform(url),
    *argsExtension(ext),
    url
], check=check)

titleOf = lambda url: subprocess.run(
    [argEnvironment, argGetTitle, url],
    capture_output=True
).stdout.decode()[0:-1] # discard \n

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
def argsPlatform(url: str) -> list:
    # 
    # instagram needs to login before downloading
    # youtube has thumbnail, "youtu.be" occurs when copy url by sharing function
    # 
    if 'instagram' in url: return [argCookiesFromBrowser, 'chrome']
    if 'youtube' in url: return [argEmbedThumbnail]
    if 'youtu.be' in url: return [argEmbedThumbnail]
    
    raise Exception(f'unsupported platform: {url}')

def argsExtension(ext: str) -> str:
    from constants import mp4, generalAudioExts, generalVideoExts
    if ext in generalAudioExts:
        return [argExtractAudio, argFormatAudio, ext]
    if ext in generalVideoExts:
        if ext == mp4: return [argFormatVideo , f'bv*[ext=mp4]+ba[ext=m4a]/b']
        return [argFormatVideo, f'bv*[ext={ext}]+ba']
    
    raise Exception(f'unknown format: {ext}')

# 
# 
# 
# 
def downloadTry(url: str, extensions: list, format: str = formatTitle):
    for ext in extensions:
        try:
            download(url, ext, format, check=True)
            return ext
        except subprocess.CalledProcessError:
            continue
    return ''