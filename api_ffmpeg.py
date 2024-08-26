# 
# 
# -----------------------------------------------
# ffmpeg.py helps the operations on audio & vedio.
# It's an implementation for https://ffmpeg.org/ 
# -----------------------------------------------
# 
# 

from script_ffmpeg import decideSubprocessOf
from sys import argv
decideSubprocessOf(argv[1])