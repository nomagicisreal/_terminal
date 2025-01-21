# 
# 
# 
# function
# 
# 
# 
def main():
    from subprocess import call
    call(argsForCompiling())
    print('\n')

def argsForCompiling() -> list:
    from script_input import whileInputValidOption
    from script_os import osSibling

    scriptAndUsecase = whileInputValidOption(availableUsecases)
    scriptName: str = scriptAndUsecase[0]
    return [
        argsForCompiler(scriptName),
        osSibling(scriptName),
        scriptAndUsecase[1],
    ]

def argsForCompiler(basename: str) -> str:
    from script_re import substringFromDot
    extension = substringFromDot(basename)

    if extension == 'py': return 'python3'
    # if extension == 'R':  return 'Rscript'
    
    raise Exception(f'unimplment file type: .{extension}')

# 
# 
# 
# constants
# 
# 
# 
# 
usecaseDowloadVideoOrAudio = 'download video|audio'
usecaseDowloadMp3 = 'download mp3'
usecaseDowloadMp4 = 'download mp4'
usecaseDowloadMultipleMp3 = 'download mp3 times'
usecaseDowloadMultipleMp3OnCwd = 'download mp3 times on current working directory'
usecaseTransformVideoOrAudio = 'transform video|audio format'
usecaseGetTotalDurationOfVideoOrAudio = 'get duration forall video|audio'
usecaseGetTotalDurationOfMp3 = 'get duration forall mp3'

scriptApiForYtdlp = 'api_ytdlp.py'
scriptApiForFfmpeg = 'api_ffmpeg.py'

availableUsecases = {
    usecaseDowloadVideoOrAudio : scriptApiForYtdlp,
    usecaseDowloadMp3 : scriptApiForYtdlp,
    usecaseDowloadMp4 : scriptApiForYtdlp,
    usecaseDowloadMultipleMp3 : scriptApiForYtdlp,
    usecaseDowloadMultipleMp3OnCwd : scriptApiForYtdlp,
    # 'download mp3 into different folder by categories' : [fileNameDownloadVideo, 3],
    # 'download mp4 into different folder by categories' : [fileNameDownloadVideo, 4],
    usecaseTransformVideoOrAudio : scriptApiForFfmpeg,
    usecaseGetTotalDurationOfVideoOrAudio : scriptApiForFfmpeg,
    usecaseGetTotalDurationOfMp3 : scriptApiForFfmpeg,
}
# availableFileTypes = {
#     '.csv' : 'csv',
#     '.sav' : 'sav',
# }
