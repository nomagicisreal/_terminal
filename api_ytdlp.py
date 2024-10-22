# 
# 
# -----------------------------------------------
# api_ytdlp.py helps to download video by terminal.
# It's an implementation for https://github.com/yt-dlp/yt-dlp 
# Supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md 
# -----------------------------------------------
# 
# 

from script_api import usecaseDowloadMp3, usecaseDowloadMp4, usecaseDowloadVideoOrAudio
from script_api import usecaseDowloadMultipleMp3, usecaseDowloadMultipleMp3OnCwd
supportedUsecases = [
    usecaseDowloadMp3, usecaseDowloadMp4, usecaseDowloadVideoOrAudio,
    usecaseDowloadMultipleMp3, usecaseDowloadMultipleMp3OnCwd,
]

supportedUsecasesForLoop = [
    usecaseDowloadMultipleMp3, usecaseDowloadMultipleMp3OnCwd,
]

def decideSubprocess(usecase: str):
    from script_ytdlp import argEnvironment
    if usecase in supportedUsecases:

        def extendingArgs(askForLocation: bool, url: str, usecase: str) -> list: 
            from script_ytdlp import argsForPlatform, argsForInputFormat, argsForLocation
            return argsForLocation(asking=askForLocation) + argsForPlatform(supportedUrl=url) + argsForInputFormat(defaultUsecase=usecase)

        from script import whileInputUrl
        from subprocess import call

        if usecase in supportedUsecasesForLoop:
            asking = False if usecase == usecaseDowloadMultipleMp3OnCwd else True
            while True:
                print("enter 'q' to exist loop")
                url = whileInputUrl()
                if url == 'q': return
                call(
                    [argEnvironment] + extendingArgs(
                        askForLocation=asking,
                        url=url,
                        usecase=usecase,
                    ) + [url]
                )
                print('\n')

        url = whileInputUrl()
        call(
            [argEnvironment] + extendingArgs(
                askForLocation=True,
                url=url,
                usecase=usecase,
            ) + [url]
        )
        return

    from script import raiseUnimplementUsecase
    raiseUnimplementUsecase(argEnvironment, usecase)
    

from sys import argv
decideSubprocess(argv[1])