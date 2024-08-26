# 
# 
# -----------------------------------------------
# ytdlp.py helps downloading video by terminal.
# It's an implementation for https://github.com/yt-dlp/yt-dlp 
# Supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md 
# -----------------------------------------------
# 
# 

commands = ['yt-dlp']

# 
# url
# 
from script_ytdlp import *
url = requireUrl()

#
# thumbnail
#
commands.extend(requireThumbnailFor(url))

#
# location
#
commands.extend([output, requireLocation()])

# 
# format
# 
import sys
commands.extend(requireFormat(getInputFormatFrom(sys.argv[1])))


# 
# 
# 
# 
import subprocess
subprocess.call(commands + [url])