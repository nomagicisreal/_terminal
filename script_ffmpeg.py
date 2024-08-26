import subprocess
import os
from script_api import yesOrNo, printCwd
from script_ytdlp import availableFiles

# extract thumbnail from audio:
# ffmpeg -i audio.mp3 -an -c:v copy image.jpg

# add thumbnail to audio
# ffmpeg -i in.mp3 -i image.png -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" out.mp3

command = 'ffmpeg'
argInput = '-i'

# 
# 
# 
# 
# 
# 
def decideSubprocessOf(option: str):
    printCwd()

    from script_api import optionTransformVideoOrAudio, optionGetTotalDurationOfVideoOrAudio, optionGetTotalDurationOfMp3
    if option == optionTransformVideoOrAudio:
        readyToTransformAll()
    elif option == optionGetTotalDurationOfVideoOrAudio:
        readyToSummarizeDurations()
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
    removeTransformed = yesOrNo('remove transformed? ')
    transformAll(
        'mp4' if inputFormat == '' else inputFormat,
        'mov' if outputFormat == '' else outputFormat,
        removeTransformed
    )

def _transformThenDelete(argv: list):
    subprocess.call(argv)
    os.remove(argv[2])

def transformAll(extIn: str, extOut: str, removeTransformed: bool):
    # all = [files for files in availableFiles() if files.split('.')[1] == extIn]
    transform = _transformThenDelete if removeTransformed else lambda argv : subprocess.call(argv)
    for file in availableFiles():
        names = file.split('.')
        if len(names) > 1 and names[1] == extIn:
            transform([
                command,
                argInput, file,
                f'{names[0]}.{extOut}'
            ])




# 
# 
# 
# summarize durations
# 
# 
# 
def readyToSummarizeDurations(extension: str = ''):
    if extension == '':
        extension = input('summarize the duration of file type (default: mp3):')
        extension = 'mp3' if extension == '' else extension

    from script_api import askForLocation, askForLocationInstruction, chooseDirectoryOn
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
    from re import search
    delta = timedelta()
    count = 0

    print('calculating...\n')
    for file in availableFiles():
        if file.split('.')[1] == extension:
            #
            # 1. get file information by ffmpeg, finding duration by regex (ffmpeg -i file.mp3 2>&1 | grep -oE "[0-9]{1}:[0-9]{2}:[0-9]{2}")
            # 2. adding duration string as datetime
            #
            duration = datetime.strptime(
                search(
                    "[0-9]{1}:[0-9]{2}:[0-9]{2}",
                    subprocess.run(
                        [command, argInput, file],
                        capture_output= True,
                    ).stderr.decode(),
                ).group(),
                '%H:%M:%S',
            ).time()
            count += 1
            delta += timedelta(
                hours=duration.hour,
                minutes=duration.minute,
                seconds=duration.second,
            )
    
    if count == 0:
        print(f'there is no {extension} in {os.getcwd()}')
        return

    print(
        f'if plays for all {count} {extension} in {os.getcwd()}\n'
        f"we needs {delta}",
    )

