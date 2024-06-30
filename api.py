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
fileNameDownloadVideo = '_ytdlp.py'
fileNameTransformVideo = '_ffmpeg.py'

availableOptions = {
    'download video or audio' : [fileNameDownloadVideo, 0],
    'download mp3' : [fileNameDownloadVideo, 1],
    'download mp4' : [fileNameDownloadVideo, 2],
    # 'download mp3 into different folder' : [fileNameDownloadVideo, 3],
    # 'download mp4 into different folder' : [fileNameDownloadVideo, 4],
    'transform video or audio' : [fileNameTransformVideo, 0],
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
    # all the options must be consist with [availableOptions]
    if fileName == fileNameDownloadVideo:
        if option == 0: return ['']
        if option == 1: return ['mp3']
        if option == 2: return ['mp4']
        raise Exception(f'unimplement option {option} for file: {fileName}')
    
    if fileName == fileNameTransformVideo:
        if option == 0: return ['']
        raise Exception(f'unimplement option {option} for file: {fileName}')

    raise Exception(f'unimplement file: {fileName}')

# 
# 
# y or n
# 
# 
def yesOrNo(question: str) -> bool:
    code = input(f'{question} (Y/N): ').capitalize()
    if code == 'Y' or code == 'N':
        return code == 'Y'
    raise Exception('pleas input Y or N')
