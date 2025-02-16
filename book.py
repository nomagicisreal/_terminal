# 
# 
# 
# 
# usecase constants
# 
# 
# 
# 
uMudiDownloadPlaylist = 'mudi download playlist by url'
uMudiCopyMusic = 'mudi copy music'
uMudiCopyMusicTo = 'mudi copy music to path'
uMudiCopyMusicToByTags = 'mudi copy music to path by tags'
uRemoveFilesNameMatchPattern = 'remove files name match pattern (sign before remove)'
uRemoveFilesNameMatchPatternNoCheck = 'remove files name match pattern (without check)'
uDowloadStreamByUrl = 'download stream by url'
uDowloadMp3ByUrl = 'download mp3 by url'
uDowloadMp3ByUrlInPath = 'download mp3 by url in path'
uDowloadMovOrMp4ToMov = 'download mov or mp4->mov by url'
uConvertStream = 'convert stream'
uConvertAllStream = 'convert all streams in path (sign to retain origin)'
uConvertAllStreamUpdate = 'convert all streams in path (remove transformed directly)'
uShowTotalDurationOfStreams = 'show total duration of all stream in path'
uShowTotalDurationOfMp3s = 'show total duration of all mp3 in path'
uThumbnailExport = 'export thumbnail from stream'
uThumbnailRemove = 'remove thumbnail of stream'
uThumbnailAttatch = 'attatch thumbnail to stream'
uThumbnailCopyToAnother = 'copy thumbnail from stream to stream'

usecasesMudi = (
    uMudiDownloadPlaylist,
    uMudiCopyMusic, uMudiCopyMusicTo, uMudiCopyMusicToByTags,
)

usecasesRemove = (
    uRemoveFilesNameMatchPattern, uRemoveFilesNameMatchPatternNoCheck
)

usecasesDownload = (
    uDowloadStreamByUrl,
    uDowloadMp3ByUrl, uDowloadMp3ByUrlInPath,
    uDowloadMovOrMp4ToMov
)

usecasesConvert = (
    uConvertStream,
    uConvertAllStream, uConvertAllStreamUpdate,
)

usecasesShow = (
    uShowTotalDurationOfStreams, uShowTotalDurationOfMp3s,
)

usecasesThumbnail = (
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
def reserveMudi(u: str):
    from counter import counterMudiDownloadPlaylist, counterMudiCopyTo, counterMudiCopyToByTags
    if u == uMudiDownloadPlaylist: return counterMudiDownloadPlaylist()
    if u == uMudiCopyMusic: return counterMudiCopyTo()
    if u == uMudiCopyMusicTo: return counterMudiCopyTo(inPath=True)
    if u == uMudiCopyMusicToByTags: return counterMudiCopyToByTags()

def reserveRemove(u: str):
    from counter import counterRemoveFilesMatch
    if u == uRemoveFilesNameMatchPattern: return counterRemoveFilesMatch()
    if u == uRemoveFilesNameMatchPatternNoCheck: return counterRemoveFilesMatch(False)


def reserveDownload(u: str):
    from counter import counterDownload, counterDownloadAOrBToA
    if u == uDowloadStreamByUrl: return counterDownload('', False)
    if u == uDowloadMp3ByUrl: return counterDownload(mp3, True)
    if u == uDowloadMp3ByUrlInPath: return counterDownload(mp3, False)
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

def reserveThumbnail(u: str):
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