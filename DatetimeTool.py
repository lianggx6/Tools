from datetime import datetime
from time import mktime


# s = "%Y-%m-%dT%H:%M:%S.%f+08:00"
# t = "2018-10-09T11:22:38.000+08:00"
# date1 = datetime(2018, 11, 2)
# print(mktime(date1.timetuple()))

print datetime.now()
date = datetime.fromtimestamp(1543293383)
print date
