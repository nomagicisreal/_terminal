from subprocess import call
from script_os import pathSplittext

# 
# 
# constaints
# 
# 
argEnvironment = 'ffmpeg'
argInput = '-i'
argAudioNone = '-an'
argMapToOutput = '-map'
argOutputFromFirst = '0:0'
argOutputFromSecond = '1:0'
argCodec = '-c'
argCodecCopy = 'copy'
argCompabilityId3v2_version = '-id3v2_version'
argMetadata = '-metadata:s:v'
argMetadataalbumArtTitle = 'title=Album Cover'
argMetadataalbumArtComment = 'comment=Cover (front)'
argSeek = '-ss'
argVideoFrames = '-vframes'

# 
# 
#
# lambdas
# 
# 

albumArtName = lambda source, format: f'{pathSplittext(source)[0]} (cover).{format}'

# ffmpeg -i input.mp3 -an -c copy cover.jpg
albumArtRetrieve = lambda source, name: call([
    argEnvironment,
    argInput, source,
    argAudioNone,
    argCodec, argCodecCopy,
    name,
])

# ffmpeg -i input.mp3 -i cover.jpg -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" output.mp3
albumArtStreamExport = lambda cover, stream, output: call([
    argEnvironment,
    argInput, stream,
    argInput, cover,
    argMapToOutput, argOutputFromFirst,
    argMapToOutput, argOutputFromSecond,
    argCodec, argCodecCopy,
    argCompabilityId3v2_version, '3',
    argMetadata, argMetadataalbumArtTitle,
    argMetadata, argMetadataalbumArtComment,
    output,
])

# ffmpeg -i input.mp4 -ss 00:00:10 -vframes 1 output.jpg
# frameOnTimedelta = lambda source, delta, format: call([
#     argEnvironment,
#     argInput, source,
#     argSeek, str(delta),
#     argVideoFrames, '1',
#     f'{source} frame{delta.seconds}.{format}'
# ])

# ffmpeg -i input.mp4 frame%03d.jpg
# framesAll = lambda source, format: call([
#     argEnvironment,
#     argInput, source,
#     f'frame%04d.{format}'
# ])

# ffmpeg -i input.mp4 -vf fps=1 -t 5 output%03d.jpg
# argVideoFilter = '-vf'
# argTime = '-t'
# framesTo = lambda source, format, fps, time: call([
#     argEnvironment,
#     argInput, source,
#     argVideoFilter, f'fps={fps}',
#     argTime, time,
#     f'frame%04d.{format}'
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
def albumArtAttach(stream: str, cover: str):
    s = f'covered| {stream}'
    albumArtStreamExport(cover, stream, s)
    from os import rename
    rename(s, stream) # update original stream

def albumArtCopy(source: str, destination: str):
    cover = albumArtName(source, 'jpg')
    albumArtRetrieve(source, cover)
    albumArtAttach(destination, cover)
    from os import remove
    remove(cover)

# 
# 
# 
def transformFormat(source: str, extOut: str, removeTransformed: bool):
    from script_os import pathSplittext
    from script_subprocess import callThenRemoveArgs2
    transform = callThenRemoveArgs2 if removeTransformed else call
    transform([argEnvironment, argInput, source, f'{pathSplittext(source)[0]}.{extOut}'])

def transformFormatAll(extIn: str, extOut: str, removeTransformed: bool):
    from script_os import foreachFiles, pathSplittext
    from script_subprocess import callThenRemoveArgs2
    def transforming(source: str):
        transform = callThenRemoveArgs2 if removeTransformed else call
        names = pathSplittext(source)
        if names[1][1:] == extIn:
            output = f'{names[0]}.{extOut}'
            print(f'{source} -> {output}')
            transform([argEnvironment, argInput, source, output])

    foreachFiles(transforming, includeSub=True)

# 
# 
# 
def summarizeDurations(extension: str):
    global seconds
    global count
    seconds = 0.0
    count = 0

    from script_ffprobe import durationOf
    def consuming(source: str):
        if pathSplittext(source)[1][1:] == extension:
            global seconds
            global count
            count += 1
            seconds += durationOf(source)

    from script_os import foreachFiles, getCwd
    foreachFiles(consuming, includeSub=True)
    
    if count == 0:
        print(f'there is no {extension} in {getCwd()}')
        return
    
    from script_datetime import timedeltaFromSeconds
    print(
        f'\n'
        f'playing all {count} {extension} in {getCwd()}\n'
        f"takes {timedeltaFromSeconds(int(seconds))}"
    )



# 
# 
# 
# 
# 
# functions ---- readyTo...
# 
# 
# 
# 
# 
def _locating():
    from script_input import ensureLocation
    ensureLocation()

def readyToTransformFormat():
    _locating()

    from script_input import ensureYorN, ensureValidFile, inputOrDefault
    transformFormat(
        ensureValidFile('source: '),
        inputOrDefault('output format', 'mov'),
        ensureYorN('remove transformed? '),
    )

def readyToTransformFormatAll():
    _locating()

    from script_input import ensureYorN, inputOrDefault
    transformFormatAll(
        inputOrDefault('input format', 'mp4'),
        inputOrDefault('output format', 'mov'),
        ensureYorN('remove transformed? '),
    )

def readyToSummarize(extension: str = ''):
    _locating()

    if not extension:
        from script_input import inputOrDefault
        extension = inputOrDefault('summarize the duration of stream type', 'mp3')
    summarizeDurations(extension)

# 
# 
# 
from script_input import ensureValidFile
def readyToRetrieveAlbumArt():
    _locating()

    from script_input import inputOrDefault
    source = ensureValidFile('source: ')
    albumArtRetrieve(
        source,
        albumArtName(source, inputOrDefault('format', 'jpg'))
    )

def readyToAttatchAlbumArt():
    _locating()

    stream = ensureValidFile('stream: ')
    cover = ensureValidFile('album art: ')
    albumArtAttach(stream, cover)

def readyToCopyAlbumArtToAnother():
    _locating()

    source = ensureValidFile('source: ')
    destination = ensureValidFile('destination: ')
    albumArtCopy(source, destination)