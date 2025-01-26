from script_subprocess import stdoutMessageOf

# 
# 
# 
# constants
# 
# 
argEnvironment = 'ffprobe'
argInput = '-i'
argVerbosity = '-v'
argVerbosityQuiet = 'quiet'
argShowEntries = '-show_entries'
argEntryFormatDuration = 'format=duration'
argOutputFormat = '-of'
argFormatCSVOnlyField = 'csv=p=0'
argSexagesimal = '-sexagesimal' # add this to make result as format HHMMSS

# 
# 
# 
# lambda
# 
# 
# 

# 
# get duration in seconds
# ffprobe -i filename.mp3 -v quiet -show_entries format=duration -of csv="p=0"
# 
durationOf = lambda source : float(stdoutMessageOf([
    argEnvironment,
    argInput,
    source,
    argVerbosity,
    argVerbosityQuiet,
    argShowEntries,
    argEntryFormatDuration,
    argOutputFormat,
    argFormatCSVOnlyField
]))