# 
# 
# -----------------------------------------------
# api_ffmpeg.py helps the operations on audio & vedio.
# It's an implementation for https://ffmpeg.org/ 
# -----------------------------------------------
# 
# 

def decideSubprocess(option: str):
    from script_api import usecaseTransformVideoOrAudio, usecaseGetTotalDurationOfVideoOrAudio, usecaseGetTotalDurationOfMp3
    from script_ffmpeg import readyToTransform, readyToSummarize
    if option == usecaseTransformVideoOrAudio: return readyToTransform()
    if option == usecaseGetTotalDurationOfVideoOrAudio: return readyToSummarize()
    if option == usecaseGetTotalDurationOfMp3: return readyToSummarize('mp3')
    
    from script_os import raiseUnimplementUsecase
    from script_ffmpeg import argEnvironment
    raiseUnimplementUsecase(argEnvironment, option)


from sys import argv
decideSubprocess(argv[1])