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
        option = whileInputNotEmpty(f'(q to quit) which {optionName}?')
        if option in options: return option
        if option == 'q': return None
        print(f'unknown option: {option}\navailable {options=}')

def whileInputValidOptionDict(options: dict):
    names = []
    lines = []
    indexes = []
    for i, action in enumerate(options):
        names.append(action)
        lines.append(f'{i+1}'.ljust(7, '-') + f' {action}')
        indexes.append(f'{i+1}')
    
    from book import printDemo
    printDemo('available options:', lines)
    action = names[int(whileInputValidOption(indexes, 'option'))-1]
    print(f'continue to {action} ... ')
    return (action, options[action])

def whileInputValidFile(title: str):
    from script_ import getCwdFiles
    availableFiles = getCwdFiles()
    while True:
        path = whileInputNotEmpty(title)
        if path in availableFiles: return path

        from script_ import extensionsForFilename
        exts = extensionsForFilename(path)
        if exts:
            if len(exts) == 1 and not whileInputReject(f'do you mean {path}.{exts[0]}?'):
                return f'{path}.{exts[0]}'
            print(f'available extensions: {exts}')
            return f"{path}.{whileInputValidOption(exts, 'extension')}"
        
        from script_ import filenameIfMatchCwdDirectory
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
    from script_ import chdirAndShowChildren
    while True:
        cwd = getcwd()
        destination = input(f'location (default: {cwd}): ')
        if not destination: return cwd
        chdirAndShowChildren(destination, successShow)

def whileDownloadVideo(ext: str):
    from book import mp4
    from script_ytdlp import download
    while True:
        download(whileInputValidUrl(), ext if ext else inputOrDefault('extension', mp4))
        if whileInputReject('continue downloading?'): return

def whileDownloadLocatedVideo(ext: str):
    from book import mp4
    from script_ytdlp import download
    while True:
        whileEnsureLocation()
        download(whileInputValidUrl(), ext if ext else inputOrDefault('extension', mp4))
        if whileInputReject('continue downloading?'): return

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
    from script_ import removeFilesContain
    whileEnsureLocation()
    removeFilesContain(
        regex=whileInputYorN('match by regex/words?'),
        pattern=whileInputNotEmpty('pattern: '),
        includeSubDir=False,
        sign=whileInputReject if signBeforeRemove else None
    )

# 
# 
# for ffmpeg
# 
# 
def counterConvertStream(ext: str = ''):
    from book import mp4
    from script_ffmpeg import convert
    whileEnsureLocation()
    convert(
        whileInputValidFile('source: '),
        ext if ext else inputOrDefault('output extension', mp4),
        whileInputYorN('remove transformed? '),
    )

def counterConvertStreamAll(extIn: str = '', extOut: str = '', signIfRemove: bool = True):
    from book import mp4, mov
    from script_ffmpeg import convertAll
    whileEnsureLocation()
    convertAll(
        extIn=extIn if extIn else inputOrDefault('input extension', mov),
        extOut=extOut if extOut else inputOrDefault('output extension', mp4),
        removeTransformed=True if signIfRemove else whileInputYorN('remove transformed? '),
        includeSubDir=whileInputYorN('include subdirectories? '),
        sign=lambda path: whileInputReject(f'sure to remove {path}? ') if signIfRemove else None
    )

def counterThumbnailExport():
    from script_ffmpeg import thumbnailExport
    from book import png
    whileEnsureLocation()
    thumbnailExport(
        whileInputValidFile('source: '),
        inputOrDefault('thumbnail extension', png)
    )

def counterThumbnailRemove():
    from script_ffmpeg import thumbnailRemove
    whileEnsureLocation()
    thumbnailRemove(
        whileInputValidFile('source: ')
    )

def counterThumbnailAttatch():
    from script_ffmpeg import thumbnailAttach
    whileEnsureLocation()
    thumbnailAttach(
        source=whileInputValidFile('source: '),
        cover=whileInputValidFile('thumbnail: '),
        rejectReplace=lambda: whileInputReject('replace exist thumnail?')
    )

def counterThumbnailCopyToAnother():
    from script_ffmpeg import thumbnailCopyToAnother
    whileEnsureLocation()
    thumbnailCopyToAnother(
        source=whileInputValidFile('source: '),
        target=whileInputValidFile('target: '),
        askForReplace=lambda: whileInputReject('replace exist thumnail?')
    )

def counterSumDuration(ext: str = ''):
    from script_ffprobe import sumDurations
    whileEnsureLocation()
    result = sumDurations(ext if ext else inputOrDefault('to sum all ___ ', 'mp3'))
    if result:
        from book import printResultCount
        from script_ import timedeltaFromSeconds
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
def counterDownload(ext: str):
    from book import mp4
    from script_ytdlp import download
    whileEnsureLocation()
    download(whileInputValidUrl(), ext if ext else inputOrDefault('extension', mp4))

def counterDownloadMany(ext: str, askLocationEverytime: bool):
    if askLocationEverytime: return whileDownloadLocatedVideo(ext)
    from book import mp4
    whileDownloadVideo(ext if ext else inputOrDefault('extension', mp4))

def counterDownloadAOrBToA(a: str, b: str):
    from script_ytdlp import downloadAOrBToA
    whileEnsureLocation()
    downloadAOrBToA(whileInputValidUrl(), extA=a, extB=b)
