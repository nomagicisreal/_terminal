import subprocess
import os
from script_re import substringFromDot, substringToDot

# 
# 
# constaints
# 
# 
argEnvironment = 'ffmpeg'
argInput = '-i'
argMetadataSV = '-metadata:s:v'

# 
# 
# lambdas
# 
# 
commandFor = lambda source : [argEnvironment, argInput, source]
informationOf = lambda fileName: subprocess.run(
    commandFor(fileName),
    capture_output= True,
).stderr.decode()

thumbnailExtract = lambda source, format: subprocess.call(commandFor(source) + [
    '-an', '-c:v', 'copy',
    f'{os.path.splitext(source)[0]}.{format}'
]) # ffmpeg -i in.mp3 -an -c:v copy image.jpg

# def thumbnailExtractThenAttatch(source: str, destination: str, format: str):
    # ffmpeg -i in.mp3 -i image.jpg -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover" out.mp3
    # subprocess.call(
    #     # command(source) + [
    #     [
    #     argEnvironment,
    #     argInput,
    #     f'{substringToDot(source)}.{format}',
    #     # '-map', '0:0',
    #     # '-map', '1:0',
    #     '-c', 'copy',
    #     '-id3v2_version', '3',
    #     argMetadataSV, 'title="Album cover"',
    #     argMetadataSV, 'comment="Cover"',
    #     destination,
    # ])



# 
# 
# 
# transform
# 
# 
# 
def readyToTransform(forall: bool = True):
    if not forall:
        from script_os import raiseUnimplementUsecase
        raiseUnimplementUsecase(argEnvironment, 'transform partial file')
    
    from script_os import whileInputYorN
    print('ready to transform all files ...')
    inputFormat = input('input format (default: mp4): ')
    outputFormat = input('output format (default: mov) forall: ')
    removeTransformed = whileInputYorN('remove transformed ? ')
    
    transformAll(
        inputFormat if inputFormat else 'mp4',
        outputFormat if outputFormat else 'mov',
        removeTransformed
    )

def transformAll(extIn: str, extOut: str, removeTransformed: bool):
    from subprocess import call
    def _subprocessCallThenDelete(argv: list):
        call(argv)
        os.remove(argv[2])
    transform = _subprocessCallThenDelete if removeTransformed else call

    def transforming(fileName: str):
        names = os.path.splitext(fileName)
        if names[1][1:] == extIn:
            print(fileName)
            transform(commandFor(fileName) + [f'{names[0]}.{extOut}'])
    
    from script_os import foreachFiles
    foreachFiles(transforming, includeSub=True)


# 
# 
# 
# summarize durations
# 
# 
# 
def readyToSummarize(extension: str):
    if not extension:
        extension = input('summarize the duration of file type (default: mp3):')
        extension = extension if extension else 'mp3'

    from script_os import whileEnsureFileLocation
    whileEnsureFileLocation()

    summarizeDurations(extension)
    
def summarizeDurations(extension: str):
    from datetime import timedelta
    from script_datetime import findingTime

    global delta
    global count
    delta = timedelta()
    count = 0

    def consuming(fileName: str):
        if substringFromDot(fileName) == extension:
            #
            # 1. get file information by ffmpeg, finding duration by regex (ffmpeg -i file.mp3 2>&1 | grep -oE "[0-9]{1}:[0-9]{2}:[0-9]{2}")
            # 2. adding duration string as datetime
            #
            duration = findingTime(informationOf(fileName))
            global delta
            global count
            count += 1
            delta += timedelta(
                hours=duration.hour,
                minutes=duration.minute,
                seconds=duration.second,
            )

    from script_os import foreachFiles
    foreachFiles(consuming, includeSub=True)
    
    if count == 0:
        print(f'there is no {extension} in {os.getcwd()}')
        return

    print(
        f'\n'
        f'if plays for all {count} {extension} in {os.getcwd()}\n'
        f"we needs {delta}", # Hours:Minutes:Seconds
    )

