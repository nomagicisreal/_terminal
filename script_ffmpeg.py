# 
# 
# 
# -----------------------------------------------
# ffmpeg helps the operations on audio & vedio.
# It's an implementation for https://ffmpeg.org/ 
# -----------------------------------------------
# 
# 
# 

# 
# 
# constaints
# 
# 
_aEnvironment = 'ffmpeg'
_aInput = '-i'
_aAudioNone = '-an'
_aMap = '-map'
_aMap0 = '0' # map all streams from first input
_aMap1 = '1' # map all streams from second input
_aMap0v0 = '0:v:0' # map from first input first video stream 
_aMap0v1 = '0:v:1' # map from first input second video stream (usually embeded thumbnail)
_aMap0a = '0:a' # map all audio
_aCodec = '-c'
_aCodecCopy = 'copy'
_aCompabilityAudioThumbnail = '-id3v2_version'
_aCompabilityVideoThumbnail = '-disposition:v:1'
_aVideoFrames = '-frames:v'
# _aVideoFilter = '-vf'
_argsMetadataAlbumArt = [
    '-metadata:s:v', 'title=Album Cover',
    '-metadata:s:v', 'comment=Cover (front)'
]

# 
# 
#
# lambdas
# 
# 
import subprocess
from script_ import splitFilename
_coverName = lambda source, ext: f'{splitFilename(source)[0]} (cover).{ext}'

# ffmpeg -i test.mp3 -map 0:a -c copy output.mp3
_exportAudio = lambda source, output: subprocess.call([
    _aEnvironment, _aInput, source,
    _aMap, _aMap0a,
    _aCodec, _aCodecCopy,
    output,
])

# ffmpeg -i test.mp4 -map 0:v:0 -map 0:a -c copy output.mp4
_exportVideo = lambda source, output: subprocess.call([
    _aEnvironment, _aInput, source,
    _aMap, _aMap0v0, _aMap, _aMap0a,
    _aCodec, _aCodecCopy,
    output,
])

# ffmpeg -i test.mp3 -an cover.png
_exportAudioCover = lambda source, output: subprocess.call([
    _aEnvironment, _aInput, source,
    _aAudioNone,
    output,
])

# ffmpeg -i test.mp4 -frames:v 1 cover.png
_exportVideoFrame1 = lambda source, output: subprocess.call([
    _aEnvironment, _aInput, source,
    _aVideoFrames, '1',
    output,
])

# ffmpeg -i test.mp4 -map 0:v:1 -c copy -frames:v 1 cover.png
_exportVideoFrame = lambda source, output, mapping: subprocess.call([
    _aEnvironment, _aInput, source,
    _aMap, mapping,
    _aVideoFrames, '1',
    output,
])

# ffmpeg -i test.mp3 -i cover.png -map 0:a -map 1 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" output.mp3
_exportFramedAudio = lambda cover, source, output: subprocess.call([
    _aEnvironment, _aInput, source, _aInput, cover,
    _aMap, _aMap0, _aMap, _aMap1,
    _aCodec, _aCodecCopy,
    _aCompabilityAudioThumbnail, '3',
    *_argsMetadataAlbumArt,
    output,
])

# ffmpeg -i test.mp4 -i cover.png -map 0:v:0 -map 0:a -map 1 -c copy -disposition:v:1 attached_pic output.mp4
_exportFramedVideo = lambda cover, source, output: subprocess.call([
    _aEnvironment, _aInput, source, _aInput, cover,
    _aMap, _aMap0v0, _aMap, _aMap0a, _aMap, _aMap1,
    _aCodec, _aCodecCopy,
    _aCompabilityVideoThumbnail, 'attached_pic',
    output,
])

# ffmpeg -i test.mp4 -ss 00:00:00 -vframes 1 output.jpg
# _aSeek = '-ss'
# frameSeekOnTimedelta = lambda source, delta, ext: subprocess.call([
#     _aEnvironment,
#     _aInput, source,
#     _aSeek, str(delta),
#     _aVideoFrames, '1',
#     f'{source} frame{delta.seconds}.{ext}'
# ])

# ffmpeg -i test.mp4 frame%03d.jpg
# framesAll = lambda source, ext: subprocess.call([
#     _aEnvironment,
#     _aInput, source,
#     f'frame%04d.{ext}'
# ])

# ffmpeg -i test.mp4 -vf fps=1 -t 5 output%03d.jpg
# _aTime = '-t'
# framesTo = lambda source, ext, fps, time: subprocess.call([
#     _aEnvironment,
#     _aInput, source,
#     _aVideoFilter, f'fps={fps}',
#     _aTime, time,
#     f'frame%04d.{ext}'
# ])

#
# 
# 
# 
# functions
#
# 
# 
# 
def thumbnailExport(source: str, imageExt: str):
    from script_ import splitFilename, translateExtAudioOrVideo
    from script_ffprobe import translateOnStreamCountAOrB
    return translateExtAudioOrVideo(
        splitFilename(source)[1][1:],
        onAudio=lambda: _exportAudioCover(source, _coverName(source, imageExt)),
        onVideo=lambda: translateOnStreamCountAOrB(
            source=source, a=2, b=3,
            onA=lambda: _exportVideoFrame(source, _coverName(source, imageExt), _aMap0v0),
            onB=lambda: _exportVideoFrame(source, _coverName(source, imageExt), _aMap0v1)
        )
    )

def thumbnailRemove(source: str):
    tempt = f'no covered| {source}'
    from script_ import splitFilename, translateExtAudioOrVideo
    from script_ffprobe import translateOnStreamCountAOrB
    translateExtAudioOrVideo(
        splitFilename(source)[1][1:],
        onAudio=lambda: translateOnStreamCountAOrB(
            source=source, a=1, b=2,
            onA=lambda: None,
            onB=lambda: _exportAudio(source, tempt)
        ),
        onVideo=lambda: translateOnStreamCountAOrB(
            source=source, a=2, b=3,
            onA=lambda: None,
            onB=lambda: _exportVideo(source, tempt),
        ),
    )
    from script_ import renameIfExist
    renameIfExist(tempt, source) # update original stream

def thumbnailAttach(source: str, cover: str, rejectReplace):
    tempt = f'covered| {source}'
    from script_ import splitFilename, translateExtAudioOrVideo
    from script_ffprobe import translateOnStreamCountAOrB
    def askBefore(export):
        if not rejectReplace():
            export(cover, source, tempt)
    translateExtAudioOrVideo(
        splitFilename(source)[1][1:],
        onAudio=lambda: translateOnStreamCountAOrB(
            source=source, a=1, b=2,
            onA=lambda: _exportFramedAudio(cover, source, tempt),
            onB=lambda: askBefore(_exportFramedAudio)
        ),
        onVideo=lambda: translateOnStreamCountAOrB(
            source=source, a=2, b=3,
            onA=lambda: _exportFramedVideo(cover, source, tempt),
            onB=lambda: askBefore(_exportFramedVideo)
        ),
    )
    from script_ import renameIfExist
    renameIfExist(tempt, source) # update original stream

def thumbnailCopyToAnother(source: str, target: str, askForReplace):
    from book import png
    cover = _coverName(source, png)
    thumbnailExport(source, png)
    thumbnailAttach(target, cover, askForReplace)
    from os import remove
    remove(cover)

# 
# 
# 
_convert = lambda source, output: subprocess.call([ 
    _aEnvironment, _aInput, source, output
])

def convert(source: str, ext: str, removeTransformed: bool):
    from script_ import splitFilename
    name = splitFilename(source)
    sExt = name[1][1:]
    if sExt == ext: return
    output = f'{name[0]}.{ext}'
    _convert(source, output)

    # # ensure video to audio has thumbnail
    # from book import generalVideoExts, generalAudioExts, png
    # if sExt in generalVideoExts and ext in generalAudioExts:
    #     from script_ffprobe import streamCountAsLine
    #     if streamCountAsLine(source) == 2:
    #         tempt = f'covered| {output}'
    #         cover = _coverName(source, png)
    #         _exportVideoFrame1(source, cover)
    #         _exportFramedAudio(cover, output, tempt)
    #         from os import rename, remove
    #         remove(cover)
    #         rename(tempt, output)
    
    if removeTransformed:
        from os import remove
        remove(source)

def convertAll(extIn: str, extOut: str, includeSubDir: bool, sign):
    from os import remove
    def convertThenRemove(source: str, output: str):
        _convert(source, output)
        remove(source)
    from os.path import abspath
    def convertThenSignToRemove(source: str, output: str):
        _convert(source, output)
        if not sign(abspath(source)): remove(source)

    convert = convertThenSignToRemove if sign else convertThenRemove

    from script_ import foreachFileNest, splitFilename
    def transforming(source: str):
        names = splitFilename(source)
        if names[1][1:] == extIn:
            output = f'{names[0]}.{extOut}'
            print(f'{source} -> {output}')
            convert(source, output)
    
    foreachFileNest(includeSubDir)(transforming)
