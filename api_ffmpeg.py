# 
# 
# -----------------------------------------------
# api_ffmpeg.py helps the operations on audio & vedio.
# It's an implementation for https://ffmpeg.org/ 
# -----------------------------------------------
# 
# 

# 
# 
# constants
# 
# 
apiName = 'api_ffmpeg.py'
usecaseTransformStream = 'transform stream format in directory'
usecaseTransformManyStream = 'transform all stream format in directory'
usecaseShowTotalDurationOfStreams = 'show total duration of all stream in directory'
usecaseShowTotalDurationOfMp3s = 'show total duration of all mp3 in directory'
usecaseRetrieveAlbumArt = 'retrieve Album art'
usecaseAttatchAlbumArt = 'attatch Album art'
usecaseCopyAlbumArtToAnother = 'copy Album art to another'

usecases = (
    usecaseTransformStream, usecaseTransformManyStream,
    usecaseShowTotalDurationOfStreams, usecaseShowTotalDurationOfMp3s,
    usecaseRetrieveAlbumArt, usecaseAttatchAlbumArt, usecaseCopyAlbumArtToAnother
)

# 
# 
# function
# 
# 
def processing(option: str):
    from script_ffmpeg import readyToTransformFormat, readyToTransformFormatAll
    if option == usecaseTransformStream: return readyToTransformFormat()
    if option == usecaseTransformManyStream: return readyToTransformFormatAll()
    if option == usecaseShowTotalDurationOfStreams: return readyToSummarize()
    
    from script_ffmpeg import readyToSummarize
    if option == usecaseShowTotalDurationOfMp3s: return readyToSummarize('mp3')

    from script_ffmpeg import readyToRetrieveAlbumArt, readyToAttatchAlbumArt, readyToCopyAlbumArtToAnother
    if option == usecaseRetrieveAlbumArt: return readyToRetrieveAlbumArt()
    if option == usecaseAttatchAlbumArt: return readyToAttatchAlbumArt()
    if option == usecaseCopyAlbumArtToAnother: return readyToCopyAlbumArtToAnother()

    from script_os import raiseInvalidUsecase
    raiseInvalidUsecase(apiName, option, usecases)
    


