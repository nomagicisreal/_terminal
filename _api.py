import subprocess
import os.path as path

# 
#
# show information, wait until valid input
#
#
def waitForInputFrom(values: dict, info: str) -> str:
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
fileNameDownloadVedio = 'yt-dlp.py'
# fileNameAnalyzeData = 'analyzer.R'

availableOptions = {
    'download vedio' : fileNameDownloadVedio,
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

def findArgs(fileName: str) -> str:
    # if fileName == fileNameAnalyzeData:
        # return waitForInputFrom(availableFileTypes, 'file types')
    # else:
        return ''

# 
# 
# argument, subprocess
# 
# 
def argumentOf(fileName: str) -> list:
    names = fileName.split('.')
    assert(len(names) == 2, f'unknown file: {fileName}')
    return [
        findCommand(names[1]),
        findPath(fileName),
        findArgs(fileName),
    ]

subprocess.call(argumentOf(waitForInputFrom(availableOptions, 'options')))

print('\n')