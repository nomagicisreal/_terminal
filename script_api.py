# 
# 
# 
# functions
# 
# 
# 

def main():
    from subprocess import call
    call(argsForCompiling())
    print('\n')

def argsForCompiling() -> list:
    from script import whileInputValidOption, osPathExtension, osPathRealSibling

    scriptAndUsecase = whileInputValidOption(availableUsecases)
    scriptName: str = scriptAndUsecase[0]
    return [
        argsForCompilingEnvironment(osPathExtension(scriptName)),
        osPathRealSibling(__file__, scriptName),
        scriptAndUsecase[1],
    ]

def argsForCompilingEnvironment(extension: str) -> str:
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
usecaseDowloadVideoOrAudio = 'download 1 video|audio'
usecaseDowloadMp3 = 'download 1 mp3'
usecaseDowloadMp4 = 'download 1 mp4'
usecaseDowloadMultipleMp3 = 'download multiple mp3'
usecaseDowloadMultipleMp3OnCwd = 'download multiple mp3 on current working directory'
usecaseTransformVideoOrAudio = 'transform format of video|audio'
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
