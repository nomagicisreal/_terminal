# 
# 
# constants
# 
# 
apiName = 'api_os.py'
usecaseRemoveFilesOfPattern = 'remove files of pattern'
usecaseRemoveFilesOfPatternWithoutCheck = 'remove files of pattern without check'
usecases = (
    usecaseRemoveFilesOfPattern, usecaseRemoveFilesOfPatternWithoutCheck
)


def processing(option: str):
    from script_os import readyToRemoveFileOfPattern
    if option == usecaseRemoveFilesOfPattern: return readyToRemoveFileOfPattern()
    if option == usecaseRemoveFilesOfPatternWithoutCheck: return readyToRemoveFileOfPattern(False)

    from script_os import raiseInvalidUsecase
    raiseInvalidUsecase(apiName, option, usecases)