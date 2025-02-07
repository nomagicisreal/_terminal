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
def whileInputNotEmpty(message: str, interpretShellLikeString: bool = True):
    # 
    # shell like string be like "Songbird\ \(Atjazz\ Love\ Soul\ Remix\).mp3"
    # 
    while True:
        value = input(message)
        if value:
            if interpretShellLikeString:
                from shlex import split
                return split(value)[0]
            return value

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
        option = whileInputNotEmpty(f'(q to quit) which {optionName}? ')
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
    index = whileInputValidOption(indexes, 'option')
    if index:
        action = names[int(index)-1]
        print(f'continue to {action} ... ')
        return (action, options[action])

def whileInputValidFile(title: str, parent: str = '', defaultForOnlyExt: bool = False):
    from os import path
    pathOf = (lambda file: path.join(parent, file)) if parent else (lambda file: file)
    def isValidFile(name: str):
        # check filename
        if path.isfile(pathOf(name)): return name

        # check filename without extension
        from script_ import extensionsForFilename
        exts = extensionsForFilename(name, parent)
        if exts:
            if len(exts) == 1:
                filename = f'{name}.{exts[0]}'
                if defaultForOnlyExt: return filename
                if whileInputReject(f'do you mean {filename}?'): return None
                else: return filename
            print(f'available extensions: {exts}')
            return f"{name}.{whileInputValidOption(exts, 'extension')}"
        
    
    while True:
        name = whileInputNotEmpty(title)
        validFile = isValidFile(name)
        if validFile: return pathOf(validFile)
        print(f'path not found: {pathOf(name)}')

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

def whileNotRejectToContinue(consume, task: str):
    while True:
        consume()
        if whileInputReject(f'continue {task}?'): return


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
# for mudi
# 
# 
def counterMudiDownloadPlaylist():
    from script_mudi import hasPermission, appendCsvThenDownloadPlaylist
    if hasPermission():
        appendCsvThenDownloadPlaylist(
            whileInputValidUrl('playlist url: '),
        )

def counterMudiCopy():
    from script_mudi import hasPermission, copyMusicTo
    if hasPermission():
        whileNotRejectToContinue(
            lambda: copyMusicTo(
                whileInputValidFile('youtube id: ', parent='test', defaultForOnlyExt=True),
                whileInputNotEmpty('path: ')
            ),
            task='copy music'
        )
        
def counterMudiCopyInPath():
    from script_mudi import hasPermission, copyMusicTo, file_parent
    if hasPermission():
        while True:
            path = whileInputNotEmpty('path: ')
            whileNotRejectToContinue(
                lambda: copyMusicTo(
                    whileInputValidFile(
                        'youtube id: ',
                        parent=file_parent,
                        defaultForOnlyExt=True
                    ),
                    path,
                ),
                task=f'copy music into {path}'
            )
            if whileInputYorN('y for switch path, n for exit'): continue
            return
    


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

def counterConvertStreamAll(extIn: str = '', extOut: str = '', signToRemove: bool = True):
    from book import mp4, mov
    from script_ffmpeg import convertAll
    whileEnsureLocation()
    convertAll(
        extIn=extIn if extIn else inputOrDefault('input extension', mov),
        extOut=extOut if extOut else inputOrDefault('output extension', mp4),
        includeSubDir=whileInputYorN('include subdirectories? '),
        sign=lambda path: whileInputReject(f'sure to remove {path}? ') if signToRemove else None
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
            f'playing all {ext} takes {timedeltaFromSeconds(int(result[1]))}'
        )

# 
# 
# 
# for yt-dlp
# 
# 
# 
def counterDownload(ext: str, askLocationEverytime: bool):
    from book import mp4
    from script_ytdlp import download
    if askLocationEverytime:
        def downloading():
            whileEnsureLocation()
            download(
                whileInputValidUrl(),
                ext if ext else inputOrDefault('extension', mp4),
                # needsCookie=True
            )
        return whileNotRejectToContinue(downloading, task='download')
    
    whileNotRejectToContinue(
        lambda: download(
            whileInputValidUrl(),
            ext if ext else inputOrDefault('extension', mp4),
            # needsCookie=True
        ),
        task='downloading'
    )
    

def counterDownloadAOrBToA(a: str, b: str):
    from script_ytdlp import downloadAOrBToA
    whileEnsureLocation()
    downloadAOrBToA(whileInputValidUrl(), extA=a, extB=b)
