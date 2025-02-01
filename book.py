# 
# 
# 
# 
# constants
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
uConvertAllStreamUpdate = 'convert all streams in directory (remove origin directly)'
uShowTotalDurationOfStreams = 'show total duration of all stream in directory'
uShowTotalDurationOfMp3s = 'show total duration of all mp3 in directory'
uThumbnailRetrieve = 'retrieve thumbnail from stream'
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
    uThumbnailRetrieve, uThumbnailAttatch, uThumbnailCopyToAnother
)

# 
# 
# 
# 
# functions
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
    from constants import mp3, mp4, mov
    if u == uDowloadStream: return counterDownload('')
    if u == uDowloadMp3: return counterDownload(mp3)
    if u == uDowloadManyMp3: return counterDownloadMany(mp3, True)
    if u == uDowloadManyMp3OnDirectory: return counterDownloadMany(mp3, False)
    if u == uDowloadMovOrMp4ToMov: return counterDownloadAOrBToA(mov, mp4)


def reserveConvert(u: str):
    from counter import counterConvertStream, counterConvertStreamAll
    if u == uConvertStream: return counterConvertStream()
    if u == uConvertAllStream: return counterConvertStreamAll()
    if u == uConvertAllStreamUpdate: return counterConvertStreamAll(signIfRemove=False)

def reserveShow(u: str):
    from counter import counterSumDuration
    from constants import mp3
    if u == uShowTotalDurationOfStreams: return counterSumDuration()
    if u == uShowTotalDurationOfMp3s: return counterSumDuration(mp3)

def reserveAlbumArt(u: str):
    from counter import counterThumbnailRetrieve, counterThumbnailAttatch, counterThumbnailCopyToAnother
    if u == uThumbnailRetrieve: return counterThumbnailRetrieve()
    if u == uThumbnailAttatch: return counterThumbnailAttatch()
    if u == uThumbnailCopyToAnother: return counterThumbnailCopyToAnother()

