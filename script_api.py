import os.path as path
import os

# 
# 
# 
# 
# 
optionDowloadVideoOrAudio = 'download video or audio'
optionDowloadMp3 = 'download mp3'
optionDowloadMp4 = 'download mp4'
optionTransformVideoOrAudio = 'transform video or audio'
optionGetTotalDurationOfVideoOrAudio = 'get total duration of video or audio'
optionGetTotalDurationOfMp3 = 'get total duration of mp3'

scriptNameYtdlp = 'api_ytdlp.py'
scriptNameFfmpeg = 'api_ffmpeg.py'

availableOptions = {
    optionDowloadVideoOrAudio : scriptNameYtdlp,
    optionDowloadMp3 : scriptNameYtdlp,
    optionDowloadMp4 : scriptNameYtdlp,
    # 'download mp3 into different folder by categories' : [fileNameDownloadVideo, 3],
    # 'download mp4 into different folder by categories' : [fileNameDownloadVideo, 4],
    optionTransformVideoOrAudio : scriptNameFfmpeg,
    optionGetTotalDurationOfVideoOrAudio : scriptNameFfmpeg,
    optionGetTotalDurationOfMp3 : scriptNameFfmpeg,
}
# availableFileTypes = {
#     '.csv' : 'csv',
#     '.sav' : 'sav',
# }


# 
# 
# 
# about path, directory
# 
# 
# 
osPathBasename = lambda path: os.path.basename(path)
osPathSplitext = lambda pathName: os.path.splitext(pathName)
osPathForExtension = lambda pathName: os.path.splitext(pathName)[1][1:]

# cwdChildren[1] are directories
# cwdChildren[2] are files
cwdChildren = lambda : next(os.walk('.'))


# def availableFiles(excludeSub: bool = True) -> list:
def foreachFiles(consume, includeSub: bool = True):
    children = cwdChildren()

    print(f'calculating for location ...')
    [consume(child) for child in children[2]]
    
    if not includeSub:
        return

    def nesting(subDirs: list, parent: str = ''):
        for subDir in subDirs:
            os.chdir(subDir)
            children = cwdChildren()
            p = path.join(parent, subDir)

            if children[1]:
                nesting(children[1], p)

            if children[2]:
                print(f'calculating for /{p} ...')
                [consume(child) for child in children[2]]
            
            os.chdir('..')
    
    nesting(children[1])

def askForLocation() -> str: return input(f'location (default: {os.getcwd()}): ')

def askForLocationInstruction(arg: str):
    print(
        f"unknown command: {arg}\n"
        "USAGES:\n"
        "\t1. press enter to ensure the default location\n"
        "\t2. 'cd /your_path', pending to provide a location\n"
    )

def chooseDirectoryOn(location: str) -> bool: # return true when valid
    try:
        os.chdir(location)
        print(f'availables dirs: {availableDirs()}')
        return True
    except FileNotFoundError:
        print(
            f'directory not found: {location},\n'
            f'availables: {availableDirs()}\n'
        )
        return False

# 
# 
# 
# api referece
# 
# 
# 
def getCompiledEnvironment(extension: str) -> str:
    if extension == 'py': return 'python3'
    # if extension == 'R':  return 'Rscript'
    raise Exception(f'unimplment file type: .{extension}')

def getScriptPath(name: str) -> str:
    return path.join(path.dirname(path.realpath(__file__)), name)


def handleOptionForScript(scriptName: str, option: int) -> list:
    if scriptName == scriptNameYtdlp:
        if option == optionDowloadVideoOrAudio: return ['']
        if option == 1: return ['mp3']
        if option == 2: return ['mp4']
    
    if scriptName == scriptNameFfmpeg:
        if option == 0: return ['0']
        if option == 1: return ['1']
        if option == 1: return ['2']
        
    raiseUnimplementOption(scriptName, option)

# 
# 
# terminal interface
# 
# 
def yesOrNo(question: str) -> bool:
    code = input(f'{question} (Y/N, default: Y): ').capitalize()
    if not code or code == 'Y':
        return True
    if code == 'N':
        return False
    raise Exception('pleas input Y or N')


# 
# 
# exceptions
# 
# 
def raiseUnimplementOption(path: str, option: str):
    raise Exception(f'unimplement option: {option} for script: {osPathBasename(path)}')




#
#
#
# ------------------------------------------------------------
#
#
#

# 
#
# show information, wait until valid input
#
#
def whileInputValid() -> list:
    optionNames = list(availableOptions.keys()) # {optionName: optionScritp}
    print(
        f'available options--\n' +
        ''.join([f'\t\t \\--{i+1}-- {name}\n' for i, name in enumerate(optionNames)])
    )
    while True:
        option: str = input('your option: ')
        if option == '':
            continue
        errorMessage: str = f'\nno such option: {option}\n'

        try:
             name = optionNames[int(option)-1]
             return [availableOptions[name], name]
        except TypeError:       errorMessage += f'please input integer instead of {option}'
        except IndexError:      errorMessage += f'invalid integer: {option} (0 < option < {len(availableOptions)})'
        except Exception as e:      errorMessage = e
        print(errorMessage)
    
# 
# 
# 
# when the input valid, get the correct argument and file
# 
# 
# 
def arguments(scriptAndOption: list) -> list:
    scriptName: str = scriptAndOption[0]
    scriptExtension = scriptName.split('.')
    assert(len(scriptExtension) == 2, f'invalid file: {scriptName}')
    return [
        getCompiledEnvironment(scriptExtension[1]),
        getScriptPath(scriptName),
        scriptAndOption[1],
    ]