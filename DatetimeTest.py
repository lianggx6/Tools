from datetime import datetime
from DataManagerTest import DataManager

'''
s = "%Y-%m-%dT%H:%M:%S.%f+08:00"
t = "2018-10-09T11:22:38.000+08:00"
date1 = datetime(2018, 7, 11)
date2 = datetime(2018, 7, 12)
date3 = datetime(2018, 7, 13)
date4 = datetime(2018, 10, 14)
date5 = datetime(2018, 10, 15)
print(date1.timestamp())
print(date2.timestamp())
print(date3.timestamp())
print(date4.timestamp()) 
print(date5.timestamp())
'''

date = datetime.fromtimestamp(1540370784)
print(date)
