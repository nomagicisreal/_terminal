

jpg = 'jpg'
png = 'png'
mp3 = 'mp3'
mp4 = 'mp4'
m4a = 'm4a'
mov = 'mov'
webm = 'webm'

generalImageExtension = (jpg, png)
# respectively according to https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#sorting-formats:~:text=Video%20Extension, https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#sorting-formats:~:text=Audio%20Extension
generalVideoExts = (mp4, mov, webm)
generalAudioExts = (m4a, 'aac', mp3, 'ogg', 'opus', webm)



# 
# linux command arguments
# 
aStdoutAndStderr = '2>&1'
aPipe = '|'
aGrep = 'grep' # global regex print
aWordCount = 'wc'
aWordCountLine = '-l'
