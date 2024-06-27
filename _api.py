import subprocess
import os.path as path

# 
#
# show information, wait until valid input
#
#
def waitForInputFrom(values: dict, info: str) -> list:
    names = list(values.keys())
    print(
        f'available {info}--\n' +
        ''.join([f'\t\t \\--{i+1}-- {name}\n' for i, name in enumerate(names)])
    )
    while True:
        option: str = input('your option: ')
        message: str = f'no such option: {option}\n'

        try:             return values[names[int(option)-1]]
        except TypeError:       message += f'except integer: {option}'
        except IndexError:      message += f'\nexpect the integer < {len(values)}: {option}'
        except Exception as e:      message = e
        print(message)
    


# 
# 
# options, availables
# 
# 
fileNameDownloadVideo = 'yt-dlp.py'
# fileNameAnalyzeData = 'analyzer.R'

availableOptions = {
    'download video or audio' : [fileNameDownloadVideo, 0],
    'download mp3' : [fileNameDownloadVideo, 1],
    'download mp4' : [fileNameDownloadVideo, 2],
    # 'analyze data' : fileNameAnalyzeData,
}
# availableFileTypes = {
#     '.csv' : 'csv',
#     '.sav' : 'sav',
# }    

#
#
# command, path, args
#
#
def findCommand(extension: str) -> str:
    if extension == 'py': return 'python3'
    # if extension == 'R':  return 'Rscript'
    raise Exception(f'unimplment file type: .{extension}')

def findPath(fileName: str) -> str:
    return path.join(
        path.dirname(path.realpath(__file__)),
        f'{fileName}',
    )

def findArgs(fileName: str, option: int) -> list:

    if fileName == fileNameDownloadVideo:
        # below should be consist with [availableOptions]
        if option == 0: return ['']
        if option == 1: return ['mp3']
        if option == 2: return ['mp4']
        raise Exception(f'unimplement option {option} for file: {fileName}')
    
    raise Exception(f'unimplement file: {fileName}')

# 
# 
# argument, subprocess
# 
# [fileName] [option]
# 
def argumentOf(argv: list) -> list:
    fileName: str = argv[0]
    names = fileName.split('.')
    assert(len(names) == 2, f'unknown file: {fileName}')
    return [
        findCommand(names[1]),
        findPath(fileName)
    ] + findArgs(fileName, argv[1])

subprocess.call(
     argumentOf(
          waitForInputFrom(availableOptions, 'options')
     )
)

print('\n')