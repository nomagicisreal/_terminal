# 
# 
# -----------------------------------------------
# api_ytdlp.py helps to download video by terminal.
# Implementation for https://github.com/yt-dlp/yt-dlp 
# Supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md 
# -----------------------------------------------
# 
# 

# 
# 
# constants
# 
# 
apiName = 'api_ytdlp.py'
usecaseDowloadStream = 'download stream'
usecaseDowloadMp3 = 'download mp3'
usecaseDowloadMp4 = 'download mp4'
usecaseDowloadManyMp3 = 'download many mp3'
usecaseDowloadManyMp3OnDirectory = 'download many mp3 in directory'
usecases = (
    usecaseDowloadStream, usecaseDowloadMp3, usecaseDowloadMp4,
    usecaseDowloadManyMp3, usecaseDowloadManyMp3OnDirectory,
)
supportedUsecasesLoop = (
    usecaseDowloadManyMp3, usecaseDowloadManyMp3OnDirectory,
)

# 
# 
# functions
# 
# 
def processing(option: str):
    if option not in usecases:
        from script_os import raiseInvalidUsecase
        raiseInvalidUsecase(apiName, option, usecases)

    from script_ytdlp import mp3, mp4
    from script_ytdlp import readyToDownload, readyToDownloadMany

    def formatOf(usecase: str):
        if usecase == usecaseDowloadStream: return ''
        if usecase == usecaseDowloadMp3: return mp3
        if usecase == usecaseDowloadMp4: return mp4
        if usecase == usecaseDowloadManyMp3: return mp3
        if usecase == usecaseDowloadManyMp3OnDirectory: return mp3
        raise Exception(f'unknown format for usecase: {usecase}')
    
    if option in supportedUsecasesLoop:
        readyToDownloadMany(
            formatOf(option),
            False if option == usecaseDowloadManyMp3OnDirectory else True
        )
        return

    readyToDownload(formatOf(option))
