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
_aVideoFrames = '-vframes'
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
from utils import splitFilename
_coverName = lambda source, ext: f'{splitFilename(source)[0]} (cover).{ext}'

# ffmpeg -i test.mp3 -an cover.png
_frameFromAudio = lambda source, output: subprocess.call([
    _aEnvironment, _aInput, source,
    _aAudioNone,
    _aCodec, _aCodecCopy,
    output,
])

# ffmpeg -i test.mp3 -map 0:a -c copy output.mp3
_audioExport = lambda source, output: subprocess.call([
    _aEnvironment, _aInput, source,
    _aMap, _aMap0a,
    _aCodec, _aCodecCopy,
    output,
])

# ffmpeg -i test.mp4 -map 0:v:0 -map 0:a -c copy output.mp4
_videoExport = lambda source, output: subprocess.call([
    _aEnvironment, _aInput, source,
    _aMap, _aMap0v0, _aMap, _aMap0a,
    _aCodec, _aCodecCopy,
    output,
])

# ffmpeg -i test.mp3 -map 0 -vframes 1 cover.png
_frameFromVideo = lambda source, output, mapping: subprocess.call([
    _aEnvironment, _aInput, source,
    _aMap, mapping,
    _aCodec, _aCodecCopy,
    _aVideoFrames, '1',
    output,
])

# ffmpeg -i test.mp3 -i cover.png -map 0:a -map 1 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" output.mp3
_framedAudioExport = lambda cover, source, output: subprocess.call([
    _aEnvironment, _aInput, source, _aInput, cover,
    _aMap, _aMap0, _aMap, _aMap1,
    _aCodec, _aCodecCopy,
    _aCompabilityAudioThumbnail, '3',
    *_argsMetadataAlbumArt,
    output,
])

# ffmpeg -i test.mp4 -i cover.png -map 0:v:0 -map 0:a -map 1 -c copy -disposition:v:1 attached_pic output.mp4
_framedVideoExport = lambda cover, source, output: subprocess.call([
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
    from utils import splitFilename, translateExtAudioOrVideo
    from script_ffprobe import translateOnStreamCountAOrB
    return translateExtAudioOrVideo(
        splitFilename(source)[1][1:],
        onAudio=lambda: _frameFromAudio(source, _coverName(source, imageExt)),
        onVideo=lambda: translateOnStreamCountAOrB(
            source=source, a=2, b=3,
            onA=lambda: _frameFromVideo(source, _coverName(source, imageExt), _aMap0v0),
            onB=lambda: _frameFromVideo(source, _coverName(source, imageExt), _aMap0v1)
        )
    )

def thumbnailRemove(source: str):
    tempt = f'no covered| {source}'
    from utils import splitFilename, translateExtAudioOrVideo
    from script_ffprobe import translateOnStreamCountAOrB
    translateExtAudioOrVideo(
        splitFilename(source)[1][1:],
        onAudio=lambda: translateOnStreamCountAOrB(
            source=source, a=1, b=2,
            onA=lambda: None,
            onB=lambda: _audioExport(source, tempt)
        ),
        onVideo=lambda: translateOnStreamCountAOrB(
            source=source, a=2, b=3,
            onA=lambda: None,
            onB=lambda: _videoExport(source, tempt),
        ),
    )
    from utils import renameIfExist
    renameIfExist(tempt, source) # update original stream

def thumbnailAttach(source: str, cover: str, rejectReplace):
    tempt = f'covered| {source}'
    from utils import splitFilename, translateExtAudioOrVideo
    from script_ffprobe import translateOnStreamCountAOrB
    def askBefore(export):
        if not rejectReplace('replace exist thumnail?'):
            export(cover, source, tempt)
    translateExtAudioOrVideo(
        splitFilename(source)[1][1:],
        onAudio=lambda: translateOnStreamCountAOrB(
            source=source, a=1, b=2,
            onA=lambda: _framedAudioExport(cover, source, tempt),
            onB=lambda: askBefore(_framedAudioExport)
        ),
        onVideo=lambda: translateOnStreamCountAOrB(
            source=source, a=2, b=3,
            onA=lambda: _framedVideoExport(cover, source, tempt),
            onB=lambda: askBefore(_framedVideoExport)
        ),
    )
    from os import rename
    rename(tempt, source) # update original stream

def thumbnailCopyToAnother(source: str, target: str, askForReplace):
    from constants import png
    cover = _coverName(source, png)
    thumbnailExport(source, png)
    thumbnailAttach(target, cover, askForReplace)
    from os import remove
    remove(cover)

# 
# 
# 

def _callThenRemoveBy(sign):
    def _callThenRemoveArg2(args: list):
        subprocess.call(args)
        subprocess.call(['rm', args[2]])
    
    def _callThenRemoveArg2IfSign(args: list):
        from os.path import abspath
        subprocess.call(args)
        origin = args[2]
        if not sign(f'sure to remove {abspath(origin)}?'): subprocess.call(['rm', origin])

    return _callThenRemoveArg2IfSign if sign else _callThenRemoveArg2

_conversionOf = lambda remove, sign: _callThenRemoveBy(sign) if remove else subprocess.call
_convert = lambda source, output, transformer: transformer([
    _aEnvironment,
    _aInput, source, # TODO: convert mp4 to mov with thumbnail stream
    output
])

def convert(source: str, ext: str, removeTransformed: bool):
    from utils import splitFilename
    name = splitFilename(source)
    if name[1][1:] == ext: return
    _convert(source, f'{name[0]}.{ext}', _conversionOf(removeTransformed, None))

def convertAll(
        extIn: str,
        extOut: str,
        removeTransformed: bool,
        includeSubDir: bool,
        sign,
    ):
    from utils import foreachFileNest, splitFilename
    transformer = _conversionOf(removeTransformed, sign)
    def transforming(source: str):
        names = splitFilename(source)
        if names[1][1:] == extIn:
            output = f'{names[0]}.{extOut}'
            print(f'{source} -> {output}')
            _convert(source, output, transformer)
    
    foreachFileNest(includeSubDir)(transforming)
