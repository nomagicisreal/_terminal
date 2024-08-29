import subprocess
import os
from script_api import askForLocation, askForLocationInstruction, chooseDirectoryOn, yesOrNo
from script_api import osPathForExtension, osPathSplitext
from script_ytdlp import foreachFiles

command = 'ffmpeg'
argInput = '-i'

# 
# 
# 
# 
# 
informationOf = lambda fileName: subprocess.run(
    [command, argInput, fileName],
    capture_output= True,
).stderr.decode()

# 
# 
# 
# 
# 
# 
def decideSubprocessOf(option: str):

    from script_api import optionTransformVideoOrAudio, optionGetTotalDurationOfVideoOrAudio, optionGetTotalDurationOfMp3
    if option == optionTransformVideoOrAudio:
        readyToTransformAll()
    elif option == optionGetTotalDurationOfVideoOrAudio:
        extension = input('summarize the duration of file type (default: mp3):')
        readyToSummarizeDurations(extension if extension else 'mp3')
    elif option == optionGetTotalDurationOfMp3:
        readyToSummarizeDurations('mp3')


# 
# 
# 
# transform
# 
# 
# 
def readyToTransformAll():
    inputFormat = input('input format (default: mp4) forall: ')
    outputFormat = input('output format (default: mov) forall: ')
    removeTransformed = yesOrNo('remove transformed ? ')
    
    transformAll(
        inputFormat if inputFormat else 'mp4',
        outputFormat if outputFormat else 'mov',
        removeTransformed
    )

def _transformThenDelete(argv: list):
    subprocess.call(argv)
    os.remove(argv[2])

def transformAll(extIn: str, extOut: str, removeTransformed: bool):
    transform = _transformThenDelete if removeTransformed else lambda argv : subprocess.call(argv)

    def transforming(fileName: str):
        names = osPathSplitext(fileName)
        if names[1][1:] == extIn:
            print(fileName)
            transform([command, argInput, fileName, f'{names[0]}.{extOut}'])
            # extract thumbnail from audio:
            # ffmpeg -i audio.mp3 -an -c:v copy image.jpg

            # add thumbnail to audio
            # ffmpeg -i in.mp3 -i image.png -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" out.mp3
    
    foreachFiles(transforming)


# 
# 
# 
# summarize durations
# 
# 
# 
def readyToSummarizeDurations(extension: str):
    while True:
        source = askForLocation()

        args = source.split()
        argsLength = len(args)
        if argsLength == 0:
            break
        
        if argsLength == 1:
            chooseDirectoryOn(args[0])
            break
        
        if argsLength == 2:
            command = args[0]
            if command == 'cd':
                chooseDirectoryOn(args[1])
                continue
        
        askForLocationInstruction(args)

    summarizeDurations(extension)
    
# 
# Hours:Minutes:Seconds
# 
def summarizeDurations(extension: str):
    from datetime import timedelta, datetime
    from script_datetime import findingTime

    global delta
    global count
    delta = timedelta()
    count = 0

    def consuming(fileName: str):
        if osPathForExtension(fileName) == extension:
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

    
    foreachFiles(consuming)
    
    if count == 0:
        print(f'there is no {extension} in {os.getcwd()}')
        return

    print(
        f'\n'
        f'if plays for all {count} {extension} in {os.getcwd()}\n'
        f"we needs {delta}",
    )

