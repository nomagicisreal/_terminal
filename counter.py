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
# while input ...
# 
# 
# 
def whileInputNotEmpty(message: str, interpretShellLikeString: bool = True):
    # handle shell like string, for example "Songbird\ \(Atjazz\ Love\ Soul\ Remix\).mp3"
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

def whileInputNumeric(question: str) -> int:
    while True:
        value = input(question + 'n = ')
        if value.isnumeric(): return value
        print('please input a numeric')

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
# 
# 
# ------------------------counter for mudi
# 
# 
# 
# 
def counterMudiDownload(requirePlaylist: bool):
    from script_mudi import passPermission, appendCsvThenDownload
    if passPermission():
        appendCsvThenDownload(
            whileInputValidUrl(f"{'playlist' if requirePlaylist else 'audio'} url: "),
            requirePlaylist
        )

def counterMudiCopyTo(inPath: bool):
    from script_mudi import passPermission
    if passPermission():
        from script_mudi import copyMusicTo, file_parent

        if inPath:
            while True:
                path = whileInputNotEmpty('path: ')
                whileNotRejectToContinue(
                    lambda: copyMusicTo(
                        whileInputValidFile(
                            'youtube id: ',
                            parent=file_parent,
                            defaultForOnlyExt=True,
                        ),
                        path,
                    ),
                    task=f'copy music into {path}'
                )
                if whileInputYorN('y for switch path, n for exit'): continue
                return

        whileNotRejectToContinue(
            lambda: copyMusicTo(
                whileInputValidFile(
                    'youtube id: ',
                    parent=file_parent,
                    defaultForOnlyExt=True,
                ),
                whileInputNotEmpty('path: ')
            ),
            task='copy music'
        )
    
def counterMudiCopyToByTags():
    from script_mudi import passPermission, copyMusicToByTags
    if passPermission():
        whileNotRejectToContinue(
            lambda: copyMusicToByTags(
                # tags
                whileInputNotEmpty('path: '),
                whileInputNotEmpty,
                whileInputReject,
                inclusive=whileInputYorN('inclusive/exclusive?')
            ),
            task='copy musics with tags'
        )


# 
# 
# 
# 
# ------------------------counter for ffmpeg
# 
# 
# 
# 
def counterUpdateVideoSpeedWithoutAudio():
    whileEnsureLocation()

    from script_ffmpeg import exportVideoSpeeded
    from script_ import splitFilename
    source = whileInputValidFile('your video: ')
    speedUpOrSlowDown = whileInputYorN('speed up / slow down? ')
    message = 'faster' if speedUpOrSlowDown else 'slower'
    howMuch = whileInputNumeric(f"n times {message}? ")
    exportVideoSpeeded(
        source=source,
        output=f'{splitFilename(source)[0]} ({howMuch}x {message}){splitFilename(source)[1]}',
        speedUp=howMuch if speedUpOrSlowDown else None,
        slowDown=None if speedUpOrSlowDown else howMuch,
    )

def counterUpdatetVideoToGif():
    whileEnsureLocation()

    from script_ffmpeg import exportGifFromVideo
    from script_ import splitFilename
    source = whileInputValidFile('your video: ')
    exportGifFromVideo(
        source=source,
        output=f'{splitFilename(source)[0]}.gif',
        qualityHigh=not whileInputReject('quality high? '),
        width=whileInputNumeric('width? ') if whileInputReject('default width? ') else -1,
        height=whileInputNumeric('height? ') if whileInputReject('default height (keep aspect ratio)? ') else -1,
        motionHeavy=whileInputReject('palette according to overall color? ')
    )

def counterConvertSingleImageToVideo():
    whileEnsureLocation()

    from script_ffmpeg import exportVideoByImage
    from script_ import splitFilename
    whileEnsureLocation()
    source = whileInputValidFile('your single image: ')
    exportVideoByImage(
        source=source,
        second=inputOrDefault('video second', '1'),
        fps=inputOrDefault('fps', '30'),
        output=inputOrDefault('output name', f'{splitFilename(source)[0]}.mp4'),
    )

def counterConvertStream():
    whileEnsureLocation()

    isSingle = whileInputYorN('convert single stream / convert all stream with same extension')
    if isSingle:
        from book import mp4
        from script_ffmpeg import convert
        return convert(
            source=whileInputValidFile('source: '),
            ext=inputOrDefault('output extension', mp4),
            removeTransformed=whileInputYorN('remove transformed? '),
        )
        
    from book import mp4, mov
    from script_ffmpeg import convertAll
    return convertAll(
        extIn=inputOrDefault('input extension', mov),
        extOut=inputOrDefault('output extension', mp4),
        includeSubDir=whileInputYorN('include subdirectories? '),
        sign=lambda path: whileInputReject(f'sure to remove {path}? ') if whileInputYorN('sign to remove?') else None
    )

def counterUpdateVideo():
    whileEnsureLocation()

    from script_ffmpeg import updateVideo
    return updateVideo(
        source=whileInputValidFile('source: '),
        update=whileInputValidFile('audio: '),
        removeTransformed=whileInputYorN('remove transformed? '),
    )

#
#
#
def counterThumbnailOperation():
    whileEnsureLocation()

    continuing = whileInputYorN('export thumbnail from stream?')
    if continuing:
        from script_ffmpeg import thumbnailExport
        from book import png
        return thumbnailExport(
            whileInputValidFile('source: '),
            inputOrDefault('thumbnail extension', png)
        )
    
    continuing = whileInputYorN('remove thumbnail of stream?')
    if continuing:
        from script_ffmpeg import thumbnailRemove
        return thumbnailRemove(whileInputValidFile('source: '))
    
    continuing = whileInputYorN('attatch thumbnail to stream from exist picture?')
    if continuing:
        from script_ffmpeg import thumbnailAttach
        return thumbnailAttach(
            source=whileInputValidFile('source: '),
            cover=whileInputValidFile('thumbnail: '),
            rejectReplace=lambda: whileInputReject('replace exist thumnail?')
        )
    
    print('i assumed that you want to copy thumbnail from stream to stream')
    from script_ffmpeg import thumbnailCopyToAnother
    thumbnailCopyToAnother(
        source=whileInputValidFile('source: '),
        target=whileInputValidFile('target: '),
        askForReplace=lambda: whileInputReject('replace exist thumnail?')
    )    

# 
# 
# 
def counterSumDuration(ext: str = ''):
    whileEnsureLocation()

    from script_ffprobe import sumDurations
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
# ------------------------counter for yt-dlp
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
    whileEnsureLocation()

    from script_ytdlp import downloadAOrBToA
    downloadAOrBToA(whileInputValidUrl(), extA=a, extB=b)
