# 
# 
# 
# input or ...
# 
# 
# 
def inputOrDefault(title: str, option):
    value = input(f'{title} (default: {option}): ')
    return value if value else option

# 
# 
# 
# input while ...
# 
# 
# 
def whileInputNotEmpty(message: str) -> str:
    while True:
        value = input(message)
        if value: return value

def whileInputYorN(question: str) -> bool:
    while True:
        code = input(question + f" (y/n): ").upper()
        if code == 'Y': return True
        if code == 'N': return False

def whileInputReject(question: str) -> bool:
    while True:
        code = input(question + f" (n to reject): ").upper()
        if not code: return False
        if code == 'N': return True

def whileInputValidOption(options, optionName: str):
    while True:
        option = whileInputNotEmpty(f'which {optionName}? ')
        if option in options: return option
        print(f'unknown option: {option}\navailable {options=}')

def whileInputValidOptionDict(options: dict):
    names = []
    lines = []
    indexes = []
    for i, action in enumerate(options):
        names.append(action)
        lines.append(f'{i+1}'.ljust(7, '-') + f' {action}')
        indexes.append(f'{i+1}')
    
    from counter_info import printDemo
    printDemo('available options:', lines)
    action = names[int(whileInputValidOption(indexes, 'option'))-1]
    print(f'continue to {action} ... ')
    return (action, options[action])

def whileInputValidFile(title: str):
    from utils import getCwdFiles
    availableFiles = getCwdFiles()
    while True:
        path = whileInputNotEmpty(title)
        if path in availableFiles: return path

        from utils import extensionsForFilename
        exts = extensionsForFilename(path)
        if exts:
            if len(exts) == 1 and not whileInputReject(f'do you mean {path}.{exts[0]}?'):
                return f'{path}.{exts[0]}'
            print(f'available extensions: {exts}')
            return f"{path}.{whileInputValidOption(exts, 'extension')}"
        
        from utils import filenameIfMatchCwdDirectory
        name = filenameIfMatchCwdDirectory(path)
        if name and name in availableFiles: return name

        print(f'path not found: {path}')

def whileInputValidUrl(title: str = 'url: '):
    from validators import url as validate
    while True:
        url = whileInputNotEmpty(title)
        if validate(url): return url
        print(f'invalid url: {url}')

def whileEnsureLocation(successShow: bool = False) -> str:
    from os import getcwd
    from utils import chdirAndShowChildren
    while True:
        cwd = getcwd()
        destination = input(f'location (default: {cwd}): ')
        if not destination: return cwd
        chdirAndShowChildren(destination, successShow)

def whileInputUrlExtensionToDownload(ext: str):
    from script_ytdlp import download
    from constants import mp4
    return download(
        whileInputValidUrl(),
        ext if ext else inputOrDefault('extension', mp4)
    )

# 
# 
# 
# 
# 
# 
# 
# counter ...
# 
# 
# 
# 
# 
# 
# 
def counterRemoveFilesMatch(signBeforeRemove: bool = True):
    from utils import removeFilesContain
    whileEnsureLocation()
    removeFilesContain(
        regex=whileInputYorN('match by regex/words?'),
        s=whileInputNotEmpty('pattern: '),
        includeSubDir=False,
        sign=whileInputReject if signBeforeRemove else None
    )

# 
# 
# for ffmpeg
# 
# 
def counterConvertStream(ext: str = ''):
    from script_ffmpeg import convert
    from constants import mp4
    whileEnsureLocation()
    convert(
        whileInputValidFile('source: '),
        ext if ext else inputOrDefault('output extension', mp4),
        whileInputYorN('remove transformed? '),
    )

def counterConvertStreamAll(extIn: str = '', extOut: str = '', signIfRemove: bool = True):
    from script_ffmpeg import convertAll
    from constants import mp4, mov
    whileEnsureLocation()
    convertAll(
        extIn=extIn if extIn else inputOrDefault('input extension', mov),
        extOut=extOut if extOut else inputOrDefault('output extension', mp4),
        removeTransformed=True if signIfRemove else whileInputYorN('remove transformed? '),
        includeSubDir=whileInputYorN('include subdirectories? '),
        sign=whileInputReject if signIfRemove else None
    )

def counterThumbnailRetrieve():
    from script_ffmpeg import thumbnailFrom
    from constants import png
    whileEnsureLocation()
    thumbnailFrom(
        whileInputValidFile('source: '),
        inputOrDefault('thumbnail extension', png)
    )

def counterThumbnailAttatch():
    from script_ffmpeg import thumbnailAttach
    whileEnsureLocation()
    thumbnailAttach(
        source=whileInputValidFile('source: '),
        cover=whileInputValidFile('thumbnail: '),
        rejectReplace=whileInputReject
    )

def counterThumbnailCopyToAnother():
    from script_ffmpeg import thumbnailCopyToAnother
    whileEnsureLocation()
    thumbnailCopyToAnother(
        source=whileInputValidFile('source: '),
        target=whileInputValidFile('target: '),
        askForReplace=whileInputReject
    )

def counterSumDuration(ext: str = ''):
    from script_ffprobe import sumDurations
    whileEnsureLocation()
    result = sumDurations(ext if ext else inputOrDefault('to sum all ___ ', 'mp3'))
    if result:
        from counter_info import printResultCount
        from utils import timedeltaFromSeconds
        printResultCount(
            result[0],
            ext,
            f'play all {ext} takes {timedeltaFromSeconds(int(result[1]))}'
        )

# 
# 
# 
# for yt-dlp
# 
# 
# 
def counterDownload(extension: str):
    whileEnsureLocation()
    whileInputUrlExtensionToDownload(extension)

def counterDownloadMany(ext: str, askLocationEverytime: bool):
    if askLocationEverytime:
        while True:
            whileEnsureLocation()
            whileInputUrlExtensionToDownload(ext)
            if whileInputReject('continue downloading?'): return
    
    whileEnsureLocation()
    if not ext:
        from constants import mp4
        ext = inputOrDefault('extension', mp4)
    
    from script_ytdlp import download
    while True:
        download(whileInputValidUrl(), ext)
        if whileInputReject('continue downloading?'): return

def counterDownloadAOrBToA(a: str, b: str):
    from script_ytdlp import downloadTry

    whileEnsureLocation()
    url = whileInputValidUrl()
    ext = downloadTry(url, (a, b))
    if ext == a: return
    if ext == b:
        from script_ytdlp import titleOf
        from script_ffmpeg import convert
        return convert(f'{titleOf(url)}.{b}', a, True)
    
    raise Exception(f"there is no {a}, {b} on {url}")
