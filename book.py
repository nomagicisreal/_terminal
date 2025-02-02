# 
# 
# 
# 
# usecase constants
# 
# 
# 
# 
uRemoveFilesNameMatchPattern = 'remove files name match pattern (sign before remove)'
uRemoveFilesNameMatchPatternNoCheck = 'remove files name match pattern (without check)'
uDowloadStream = 'download stream'
uDowloadMp3 = 'download mp3'
uDowloadManyMp3 = 'download many mp3'
uDowloadManyMp3OnDirectory = 'download many mp3 in directory'
uDowloadMovOrMp4ToMov = 'download mov or mp4->mov'
uConvertStream = 'convert stream'
uConvertAllStream = 'convert all streams in directory (sign to remove origin)'
uConvertAllStreamUpdate = 'convert all streams in directory (remove transformed directly)'
uShowTotalDurationOfStreams = 'show total duration of all stream in directory'
uShowTotalDurationOfMp3s = 'show total duration of all mp3 in directory'
uThumbnailExport = 'export thumbnail from stream'
uThumbnailRemove = 'remove thumbnail of stream'
uThumbnailAttatch = 'attatch thumbnail to stream'
uThumbnailCopyToAnother = 'copy thumbnail from stream to stream'

usecasesRemove = (
    uRemoveFilesNameMatchPattern, uRemoveFilesNameMatchPatternNoCheck
)

usecasesDownload = (
    uDowloadStream, uDowloadMp3,
    uDowloadManyMp3, uDowloadManyMp3OnDirectory,
    uDowloadMovOrMp4ToMov
)

usecasesConvert = (
    uConvertStream,
    uConvertAllStream, uConvertAllStreamUpdate,
)

usecasesShow = (
    uShowTotalDurationOfStreams, uShowTotalDurationOfMp3s,
)

usecasesAlbumnArt = (
    uThumbnailExport, uThumbnailRemove,
    uThumbnailAttatch, uThumbnailCopyToAnother
)

# 
# 
# 
# 
# reserve functions
# 
# 
# 
# 
def reserveRemove(u: str):
    from counter import counterRemoveFilesMatch
    if u == uRemoveFilesNameMatchPattern: return counterRemoveFilesMatch()
    if u == uRemoveFilesNameMatchPatternNoCheck: return counterRemoveFilesMatch(False)


def reserveDownload(u: str):
    from counter import counterDownload, counterDownloadMany, counterDownloadAOrBToA
    if u == uDowloadStream: return counterDownload('')
    if u == uDowloadMp3: return counterDownload(mp3)
    if u == uDowloadManyMp3: return counterDownloadMany(mp3, True)
    if u == uDowloadManyMp3OnDirectory: return counterDownloadMany(mp3, False)
    if u == uDowloadMovOrMp4ToMov: return counterDownloadAOrBToA(mov, mp4)

def reserveConvert(u: str):
    from counter import counterConvertStream, counterConvertStreamAll
    if u == uConvertStream: return counterConvertStream()
    if u == uConvertAllStream: return counterConvertStreamAll()
    if u == uConvertAllStreamUpdate: return counterConvertStreamAll(signToRemove=False)

def reserveShow(u: str):
    from counter import counterSumDuration
    if u == uShowTotalDurationOfStreams: return counterSumDuration()
    if u == uShowTotalDurationOfMp3s: return counterSumDuration(mp3)

def reserveAlbumArt(u: str):
    from counter import counterThumbnailRemove, counterThumbnailExport, counterThumbnailAttatch, counterThumbnailCopyToAnother
    if u == uThumbnailExport: return counterThumbnailExport()
    if u == uThumbnailRemove: return counterThumbnailRemove()
    if u == uThumbnailAttatch: return counterThumbnailAttatch()
    if u == uThumbnailCopyToAnother: return counterThumbnailCopyToAnother()

# 
# 
# 
# 
# 
# ----------------------------------------------------------------------------
# 
# 
# 
# 
# 
# 

# 
# 
# 
# other constants
# 
# 
# 
# 
jpg = 'jpg'
png = 'png'
mp3 = 'mp3'
mp4 = 'mp4'
m4a = 'm4a'
mov = 'mov'
webm = 'webm'

generalImageExtension = (jpg, png)
generalVideoExts = (mp4, mov, webm) # respectively according to https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#sorting-formats:~:text=Video%20Extension, https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#sorting-formats:~:text=Audio%20Extension
generalAudioExts = (m4a, 'aac', mp3, 'ogg', 'opus', webm)

# linux command arguments
aStdoutAndStderr = '2>&1'
aPipe = '|'
aGrep = 'grep' # global regex print
aWordCount = 'wc'
aWordCountLine = '-l'


# 
# 
# 
# print funcitons
# 
# 
# 
printDemo = lambda title, lines: print(f'{title}\n' + '\n'.join(lines) + '\n')

def printResultCount(count: int, item: str, itemsDescription: str):
    if count == 0:
        print(f'there is no {item}')
        return
    print(f'\nthere are {count} {item}\n{itemsDescription}')