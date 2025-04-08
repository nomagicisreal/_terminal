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
_aCookiesFromBrowser = '--cookies-from-browser' # some video need account information stored on browser before view
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

from script_ import stdoutMessageOf
import subprocess
# yt-dlp --print "%(title)s" "https://www.youtube.com/..." (passing playlist url return every video field in many lines)
infoOf = lambda url, field, needsCookie = False: stdoutMessageOf([
    _aEnvironment, *_argsCookies(needsCookie),
    _aPrint, field, url
])

# yt-dlp --playlist-items 1 --print "%(playlist_title)s" "https://www.youtube.com/playlist?list=PL1234567890"
infoPlaylistTitleOf = lambda url, needsCookie = False: stdoutMessageOf([
    _aEnvironment, *_argsCookies(needsCookie), # for watch later playlist or private playlist
    _aPlaylistItems, '1',
    _aPrint, fieldPlaylistTitle, url,
])

# yt-dlp -o ...
download = lambda url, ext, format = fieldTitle, needsCookie = False, check = False: subprocess.run([
    _aEnvironment, *_argsCookies(needsCookie),
    _aOutputFormat, format,
    *_argsPlatform(url),
    *_argsExtension(ext),
    url,
], check=check)

# # yt-dlp -o ...
# downloadYoutubeAccountPlaylists = lambda ext, format = fieldTitle: subprocess.call([
#     _aEnvironment, *_argsCookies(True),
#     _aOutputFormat, format,
#     _aEmbedThumbnail,
#     *_argsExtension(ext),
#     'https://www.youtube.com/feed/playlists',
# ])

import re

# "youtu.be" occurs when url comes from sharing function
isOnYoutube = lambda url: re.search(r'^https://(www\.)?(youtube\.com|youtu\.be)/', url)
isOnInstagram = lambda url: re.search(r'^https://(www\.)?(instagram\.com)/', url)

isYoutubeVideoUrlWithPlaylist = lambda url: re.search(r'list=', url)
_searchAppendedPlaylistIdOf = lambda url: re.search(r'&list=([\w-]+)', url)
searchVideoIdOf = lambda url: re.search(r'(?:v=|\/)([\w-]{11})', url).group(1)

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
_argsCookies = lambda needs: [_aCookiesFromBrowser, _aBrowserChrome] if needs else []

def _argsPlatform(url: str) -> list:
    if isOnYoutube(url): return _argsPlatformYoutube(url)
    if isOnInstagram(url): return _argsPlatformInstagram(url)
    return [url]
    # raise Exception(
    #     f'unimplement url: {url}\n'
    #     f'only implement youtube, instagram for now'
    # )

def _argsExtension(ext: str) -> str:
    from book import mp4, generalAudioExts, generalVideoExts
    if ext in generalAudioExts:
        return [_aExtractAudio, _aFormatAudio, ext]
    if ext in generalVideoExts:
        if ext == mp4: return [_aFormatVideo , f'bv*[ext=mp4]+ba[ext=m4a]/b']
        return [_aFormatVideo, f'bv*[ext={ext}]+ba']
    
    raise Exception(f'unknown format: {ext}')


# 
# case 1: https://www.youtube.com/watch?v=...
# case 2: https://www.youtube.com/playlist?list=...
# case 3: https://www.youtube.com/watch?v=...&list=...&index=...
# 
def _argsPlatformYoutube(url: str):
    # 
    
    # 
    result = [_aEmbedThumbnail]
    if _searchAppendedPlaylistIdOf(url):
        from counter import whileInputReject
        if whileInputReject(f"download all the other video in playlist: '{infoPlaylistTitleOf(url)}'? "):
            result.append(_aNoPlaylist)

    return result

def _argsPlatformInstagram():
    return []


# 
# 
# 
# function
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
