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
_aMap0v = '0:v' # map all video from first input
_aMap0a = '0:a' # map all audio from first input
_aMap1a = '1:a'
_aMap0v0 = '0:v:0' # map first video stream from first input
_aMap0v1 = '0:v:1' # map second video stream from first input (usually embeded thumbnail)
_aSeek = '-ss'
_aCodec = '-c'
_aCodecCopy = 'copy'
_aCompabilityAudioThumbnail = '-id3v2_version'
_aStreamPositionThumbnail = '-disposition:v:1'
_aVideoFrames = '-frames:v'
_aVideoFilter = '-vf' # for 1 input/output
# _aVideoFilterComplex = '-filter_complex' # for multiple input/output
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

def _argForVideoFilter(
        speedUp = None,
        slowDown = None,
        fps = None,
        scaleWidth = None,
        scaleHeight = None,
        gifMotionHeavy = None,
    ):
    args = []
    if fps: args.append(f'fps={fps}')
    if speedUp: args.append(f"setpts=PTS/{speedUp}")
    if slowDown: args.append(f"setpts={slowDown}*PTS")

    if scaleWidth or scaleHeight: args.append(f'scale={scaleWidth}:{scaleHeight}:flags=lanczos') # Lanczos resampling algorithm
    if gifMotionHeavy != None:
        genOption = f"palettegen{'=stats_mode=diff' if gifMotionHeavy else ''}" # smooth palette or overall palette
        args.append(f'split[x][y];[x]{genOption}[p];[y][p]paletteuse=dither=sierra2_4a')
        args[0] = f'[0:v]{args[0]}'

    return ','.join(args)

# ffmpeg -i input.mov outpu.mp4
_export = lambda source, output: subprocess.call([ 
    _aEnvironment, _aInput, source, output
])

# ffmpeg -i input.mp3 -map 0:a -c copy output.mp3
_exportAudioWithoutThumbnail = lambda source, output: subprocess.call([
    _aEnvironment, _aInput, source,
    _aMap, _aMap0a,
    _aCodec, _aCodecCopy,
    output,
])

# ffmpeg -i input.mov -map 0:v:0 -map 0:a -c copy output.mov
_exportVideoWithoutThumbnail = lambda source, output: subprocess.call([
    _aEnvironment, _aInput, source,
    _aMap, _aMap0v0, _aMap, _aMap0a,
    _aCodec, _aCodecCopy,
    output,
])

# ffmpeg -i input.mov -i input.mp3 -map 0:v -map 1:a -c copy output.mov
_exportVideoWithAudio = lambda source, audio, output: subprocess.call([
    _aEnvironment, _aInput, source, _aInput, audio,
    _aMap, _aMap0v, _aMap, _aMap1a,
    _aCodec, _aCodecCopy,
    output,
])

# ffmpeg -i input.mp3 -an cover.png
_exportAudioCover = lambda source, output: subprocess.call([
    _aEnvironment, _aInput, source,
    _aAudioNone,
    _aCodec, _aCodecCopy,
    output,
])

# ffmpeg -i input.mov -map 0:v:1 -frames:v 1 cover.png
_exportVideoFrame = lambda source, output, mapping: subprocess.call([
    _aEnvironment, _aInput, source,
    _aMap, mapping,
    _aVideoFrames, '1',
    output,
])

# ffmpeg -i input.mp3 -i cover.png -map 0:a -map 1 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" output.mp3
_exportFramedAudio = lambda cover, source, output: subprocess.call([
    _aEnvironment, _aInput, source, _aInput, cover,
    _aMap, _aMap0, _aMap, _aMap1,
    _aCodec, _aCodecCopy,
    _aCompabilityAudioThumbnail, '3',
    *_argsMetadataAlbumArt,
    output,
])

# ffmpeg -i input.mov -i cover.png -map 0:v:0 -map 0:a -map 1 -c copy -disposition:v:1 attached_pic output.mov
_exportFramedVideo = lambda cover, source, output: subprocess.call([
    _aEnvironment, _aInput, source, _aInput, cover,
    _aMap, _aMap0v0, _aMap, _aMap0a, _aMap, _aMap1,
    _aCodec, _aCodecCopy,
    _aStreamPositionThumbnail, 'attached_pic',
    output,
])

# ffmpeg -loop 1 -i input.png -c:v libx264 -t 1 -pix_fmt yuv420p -vf "fps=25" output.mov
exportVideoByImage = lambda source, second, fps, output: subprocess.call([
    _aEnvironment, '-loop', '1',  _aInput, source, # loop infinitly
    '-c:v', 'libx264',
    '-t', second, # limit time
    '-pix_fmt', 'yuv420p',
    _aVideoFilter, _argForVideoFilter(fps=fps),
    output,
])

# ffmpeg -i tempt.mov -an -vf "setpts=PTS/3" result.mov
exportVideoSpeeded = lambda source, output, speedUp, slowDown: subprocess.call([
    _aEnvironment,
    _aInput, source,
    _aAudioNone,
    _aVideoFilter, _argForVideoFilter(speedUp=speedUp, slowDown=slowDown),
    output,
])

# TODO: implement gif generation
# ffmpeg -i input.mov -filter_complex "[0:v]fps=30,scale=480:-1:flags=lanczos,split[x][y];[x]palettegen[p];[y][p]paletteuse=dither=sierra2_4a" output.gif
exportGifFromVideo = lambda source, output, qualityHigh = True, width = -1, height = -1, motionHeavy = True: subprocess.call([
    _aEnvironment, _aInput, source,
    _aVideoFilter, _argForVideoFilter(
        fps=30 if qualityHigh else 15,
        scaleWidth=width,
        scaleHeight=height,
        gifMotionHeavy=motionHeavy,
    ),
    output,
])

# ffmpeg -i input.mov -ss 00:00:00 -vframes 1 output.jpg
exportFrameSeekOnVideo = lambda source, time, ext: subprocess.call([
    _aEnvironment,
    _aInput, source,
    _aSeek, time,
    _aVideoFrames, '1',
    f'{source}-({time}).{ext}'
])

# ffmpeg -i input.mov frame%03d.jpg
# framesAll = lambda source, ext: subprocess.call([
#     _aEnvironment,
#     _aInput, source,
#     f'frame%04d.{ext}'
# ])

# ffmpeg -i input.mov -vf fps=1 -t 5 output%03d.jpg
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
def convert(source: str, ext: str, removeTransformed: bool):
    from script_ import splitFilename
    name = splitFilename(source)
    sExt = name[1][1:]
    if sExt == ext: return
    output = f'{name[0]}.{ext}'
    _export(source, output)

    # ensure video to audio has thumbnail, despite video hasn't thumbnail
    # from book import generalVideoExts, generalAudioExts, png
    # if sExt in generalVideoExts and ext in generalAudioExts:
    #     from script_ffprobe import streamCountAsLine
    #     if streamCountAsLine(source) == 2:
    #         tempt = f'covered| {output}'
    #         cover = _coverName(source, png)
    #         _exportVideoFrame(source, cover, _aMap0v0)
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
        _export(source, output)
        remove(source)
    from os.path import abspath
    def convertThenSignToRemove(source: str, output: str):
        _export(source, output)
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


def updateVideo(source: str, update: str, removeTransformed: bool):
    from os.path import basename
    output = f'new-{basename(source)}'
    _exportVideoWithAudio(source, update, output)
    if removeTransformed:
        from os import rename
        rename(output, source)


# 
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
            onB=lambda: _exportAudioWithoutThumbnail(source, tempt)
        ),
        onVideo=lambda: translateOnStreamCountAOrB(
            source=source, a=2, b=3,
            onA=lambda: None,
            onB=lambda: _exportVideoWithoutThumbnail(source, tempt),
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

