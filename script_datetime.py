from datetime import timedelta
from re import search

# 
# 
# lambdas
# 
# 
findingTimeText = lambda source: search(r"[0-9]{1,2}:[0-9]{2}:[0-9]{2}", source).group()
timedeltaFromSeconds = lambda seconds: timedelta(seconds=seconds)
formatHourMinuteSecond = lambda seporator: f'%H{seporator}%M{seporator}%S'
formatYearDate = lambda seporator: f'%Y{seporator}%m{seporator}%d'
formatYearToSecond = lambda sDate, sTime: f'%Y{sDate}%m{sDate}%d %H{sTime}%M{sTime}%S'
