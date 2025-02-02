# 
# 
# 
# constants
# 
# 
_aEnvironment = 'ffprobe'
_aInput = '-i'
_aVerbosity = '-v'
_aVerbosityQuiet = 'quiet'
_aShowEntries = '-show_entries'
_aEntryFormatDuration = 'format=duration'
_aOutputFormat = '-of'
_aFormatCSVOnlyField = 'csv=p=0'
# _aSexagesimal = '-sexagesimal' # add this to make result as format HHMMSS

# 
# 
# 
# lambda
# 
# 
# 
from script_ import stdoutMessageOf
# 
# ffprobe -i filename.mp3 -v quiet -show_entries format=duration -of csv="p=0"
durationOf = lambda source : float(stdoutMessageOf([
    _aEnvironment,
    _aInput,
    source,
    _aVerbosity,
    _aVerbosityQuiet,
    _aShowEntries,
    _aEntryFormatDuration,
    _aOutputFormat,
    _aFormatCSVOnlyField
]))

from book import aStdoutAndStderr, aPipe, aGrep, aWordCount, aWordCountLine
import subprocess

subprocessShellPipeText = lambda args: subprocess.run(
    ' '.join(args),
    shell=True, stdout=subprocess.PIPE,
    text=True
).stdout.strip()

# 
# 
# 
# functions
# 
# 
# 
def sumDurations(ext: str):
    global seconds
    global count
    seconds = 0.0
    count = 0

    from script_ import splitFilename, foreachFileNest
    def consuming(source: str):
        if splitFilename(source)[1][1:] == ext:
            global seconds
            global count
            count += 1
            seconds += durationOf(source)
    
    foreachFileNest(True)(consuming)
    
    if count > 0: return (count, seconds)


# ffprobe -i input.mp4 2>&1 | grep 'Stream' | wc -l
streamCountAsLine = lambda source: int(subprocessShellPipeText([
    _aEnvironment, _aInput, f"'{source}'",
    aStdoutAndStderr, aPipe, aGrep, 'Stream', aPipe, aWordCount, aWordCountLine
]))

# ffprobe -i input.mp4 2>&1 | grep 'Stream' | wc
streamCount = lambda source: subprocessShellPipeText([
    _aEnvironment, _aInput, f"'{source}'",
    aStdoutAndStderr, aPipe, aGrep, 'Stream', aPipe, aWordCount,
])


def translateOnStreamCountAOrB(source: str, a: int, b: int, onA, onB):
    count = streamCountAsLine(source)
    if count == a: return onA()
    if count == b: return onB()
    raise Exception(f'unimplement stream count: {count}')