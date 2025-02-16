import subprocess
import os
import re
import datetime

# 
# 
# lambda
# 
# 
printDevider = lambda message, size = 50, fill = '-': print(message.center(size, fill))
stdoutMessageOf = lambda args: subprocess.run(args, capture_output=True).stdout.decode().strip() # discard \n
splitFilename = lambda source: os.path.splitext(source) # 'name.ext' -> ('name', '.ext')
nameFromPath = lambda path: splitFilename(os.path.basename(path))[0]
walking = lambda location: next(os.walk(location))
getDirectories = lambda parent = '': walking(parent if parent else '.')[1]
getFiles = lambda parent = '': walking(parent if parent else '.')[2]
matchCwdDirectory = lambda path, parent = '' : re.match('^' + os.path.join(os.getcwd(), parent), path)

timedeltaFromSeconds = lambda seconds: datetime.timedelta(seconds=seconds)
formatHourMinuteSecond = lambda seporator: f'%H{seporator}%M{seporator}%S'
formatYearDate = lambda seporator: f'%Y{seporator}%m{seporator}%d'
formatYearToSecond = lambda sDate, sTime: f'%Y{sDate}%m{sDate}%d %H{sTime}%M{sTime}%S'
findingTimeText = lambda source: re.search(r"[0-9]{1,2}:[0-9]{2}:[0-9]{2}", source).group()

#
#
#
# functions
#
# 
# 


# 
# 
# 
# os operations
# 
# 
# 
def renameIfExist(filename: str, output: str):
    if filename in getFiles():
        return os.rename(filename, output)

def extensionsForFilename(name: str, parent: str = ''):
    extensions = []
    for file in getFiles(parent):
        nameExt = splitFilename(file)
        if nameExt[0] == name: extensions.append(nameExt[1][1:])
    return extensions

def translateExtAudioOrVideo(ext: str, onAudio, onVideo):
    from book import generalAudioExts, generalVideoExts
    if ext in generalAudioExts: return onAudio()
    if ext in generalVideoExts: return onVideo()
    raise Exception(
        f'unimplement extension: {ext}\n'
        f'supported audio extension: {generalAudioExts}\n'
        f'supported video extension: {generalVideoExts}\n'
    )

def chdirAndShowChildren(location: str, successShow: bool = False) -> bool: # return true when choosen
    import subprocess
    try:
        os.chdir(location)
        if successShow: subprocess.call(['ls', '-d']) # list only directories
        return True
    except FileNotFoundError:
        print(f'location not found: {location}')
        printDevider('available directories')
        subprocess.call(['ls', '-d'])
        return False

def removeFilesContain(regex: bool, pattern: str, includeSubDir: bool, sign):
    from re import match
    validate = match if regex else lambda pattern, source: pattern in source
    remover = lambda source: source
    if sign:
        def removerCareful(pattern: str):
            def checking(source: str):
                if validate(pattern, source):
                    if not sign(f'sure to remove {os.path.abspath(source)}?'):
                        os.remove(source)

            return checking
        remover = removerCareful(pattern)
    else:
        remover = lambda source: os.remove(source) if validate(pattern, source) else None
    
    foreachFileNest(includeSubDir)(remover)


# 
# os operations -- foreach...
# 

# assert children are files
def _foreachFile(translate, children):
    for child in children:
        print(f'travel file: {child}')
        translate(child)

# assert children are directories
def _foreachDirectory(translate, children: list):
    for dir in children:
        os.chdir(dir)
        translate(dir, walking('.'))
        os.chdir('..')

def foreachDirectory(translate, parent: str = '.'):
    print(f'iterating on {os.path.abspath(parent)} ...')
    _foreachDirectory(translate, walking(parent)[1])

def foreachFile(translate, parent: str = '.'):
    print(f'iterating on {os.path.abspath(parent)} ...')
    _foreachFile(translate, walking(parent)[2])


def foreachFileNestBreadthFirst(translate, parent: str = '.'):
    def nesting(dir: str, children: list):
        print(f'open {dir} ...')
        if children[2]: _foreachFile(translate, children[2])
        if children[1]: _foreachDirectory(nesting, children[1])
    
    print(f'nesting on {os.path.abspath(parent)} ...')
    nesting(parent, walking(parent))

foreachFileNest = lambda subDir: foreachFileNestBreadthFirst if subDir else foreachFile