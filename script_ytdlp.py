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
_aEnvironment = 'yt-dlp'
_aEmbedThumbnail = '--embed-thumbnail'
_aCookiesFromBrowser = '--cookies-from-browser'
_aBrowserChrome = 'chrome'
_aOutputFormat = '-o'
_aExtractAudio = '-x'
_aFormatAudio = '--audio-format'
_aFormatVideo = '-f'
_aNoPlaylist = '--no-playlist'
_aPrint = '--print'
_aPlaylistItems = '--playlist-items'

# see available fields https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#output-template-examples:~:text=processing%20is%20complete.-,The%20available%20fields%20are
# getTitle = '--get-title'
# getId = '--get-id'
fieldTitle = f'%(title)s'
fieldPlaylistTitle = f'%(playlist_title)s'
fieldId = f'%(id)s'

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
# yt-dlp --print "%(title)s" "https://www.youtube.com/..." (passing playlist url return every video field in many lines)
infoOf = lambda url, field: subprocess.run([
    _aEnvironment, _aPrint, field, url
], capture_output=True,
).stdout.decode().strip() # discard \n

# yt-dlp --playlist-items 1 --print "%(playlist_title)s" "https://www.youtube.com/playlist?list=PL1234567890"
infoPlaylistItem1Of = lambda url, field: subprocess.run([
    _aEnvironment,
    _aPlaylistItems, '1',
    _aPrint, field, url,
], capture_output=True,
).stdout.decode().strip()

download = lambda url, ext, format = fieldTitle, check = False: subprocess.run([
    _aEnvironment,
    _aOutputFormat, format,
    *argsPlatform(url),
    *argsExtension(ext),
    url,
], check=check)



import re

# "youtu.be" occurs when url comes from sharing function
isOnYoutube = lambda url: re.search(r'^https://(www\.)?(youtube\.com|youtu\.be)/', url)
searchAppendedPlaylistIdOf = lambda url: re.search(r'&list=([\w-]+)', url)
searchVideoIdOf = lambda url: re.search(r'(?:v=|\/)([\w-]{11})', url).group(1)

isOnInstagram = lambda url: re.search(r'^https://(www\.)?(instagram\.com)/', url)

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
    if isOnYoutube(url): return dowloadFromYoutube(url)
    if isOnInstagram(url): return downloadFromInstagram(url)
    raise Exception(
        f'unimplement url: {url}\n'
        f'only implement youtube, instagram for now'
    )

def argsExtension(ext: str) -> str:
    from book import mp4, generalAudioExts, generalVideoExts
    if ext in generalAudioExts:
        return [_aExtractAudio, _aFormatAudio, ext]
    if ext in generalVideoExts:
        if ext == mp4: return [_aFormatVideo , f'bv*[ext=mp4]+ba[ext=m4a]/b']
        return [_aFormatVideo, f'bv*[ext={ext}]+ba']
    
    raise Exception(f'unknown format: {ext}')

# 
# 
# 
# 
def downloadAOrBToA(url: str, extA: str, extB: str):
    from subprocess import CalledProcessError
    try:
        download(url, extA, fieldTitle, check=True)
    except CalledProcessError:
        from script_ffmpeg import convert
        try:
            download(url, extB, fieldTitle, check=True)
            convert(f'{infoOf(url, fieldTitle)}.{extA}', extB, removeTransformed=True)
        except CalledProcessError:
            raise Exception(f"there is no {extA}, {extB} on {url}")


# 
# 
# 
# function
# 
# 
# 
def dowloadFromYoutube(url: str):
    # 
    # case 1: https://www.youtube.com/watch?v=...
    # case 2: https://www.youtube.com/playlist?list=...
    # case 3: https://www.youtube.com/watch?v=...&list=...&index=...
    # 
    result = [_aEmbedThumbnail]
    if searchAppendedPlaylistIdOf(url):
        from counter import whileInputReject
        if whileInputReject(f"download all the other video in playlist: '{infoPlaylistItem1Of(url, fieldPlaylistTitle)}'? "):
            result.append(_aNoPlaylist)

    return result

def downloadFromInstagram():
    # 
    # instagram needs to login before downloading
    # 
    return [_aCookiesFromBrowser, _aBrowserChrome]
