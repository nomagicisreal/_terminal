from datetime import timedelta, datetime
from re import search

# 
# 
# 
findingTimeText = lambda source: search("[0-9]{1}:[0-9]{2}:[0-9]{2}", source).group()
findingTime = lambda source: datetime.strptime(findingTimeText(source), '%H:%M:%S').time()

# 
# 
# 
# 
def addingTimes(times: list, format: str = '%H:%M:%S') -> str:
    delta = timedelta()
    for time in times:
        d = datetime.strptime(time, format).time()
        delta += timedelta(hours=d.hour, minutes=d.minute, seconds=d.second)
    return delta

# myTimes = ['00:01:11', '01:02:01', '03:00:52']
# print(addingTimes(myTimes))