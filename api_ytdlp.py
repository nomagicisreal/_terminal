# 
# 
# -----------------------------------------------
# ytdlp.py helps downloading video by terminal.
# It's an implementation for https://github.com/yt-dlp/yt-dlp 
# Supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md 
# -----------------------------------------------
# 
# 

def decideSubprocess(option: str):
    from script_ytdlp import argEnvironment
    from script_api import usecaseDowloadMp3, usecaseDowloadMp4, usecaseDowloadVideoOrAudio
    
    if option in [usecaseDowloadMp3, usecaseDowloadMp4, usecaseDowloadVideoOrAudio]:
        from script_ytdlp import requireThumbnailIf, whileInputLocation, whileInputFormat, checkInputFormatFrom
        from script import whileInputUrl
        from subprocess import call
        url = whileInputUrl()
        commands = [argEnvironment]
        commands.extend(requireThumbnailIf(supportedUrl=url))
        commands.extend(whileInputLocation())
        commands.extend(whileInputFormat(defaultOption=option))
        call(commands + [url])
        return


    from script import raiseUnimplementUsecase
    raiseUnimplementUsecase(argEnvironment, option)
    

from sys import argv
decideSubprocess(argv[1])