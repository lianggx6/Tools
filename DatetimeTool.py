from time import mktime
import pandas as pd
from datetime import datetime
s = "%Y-%m-%dT%H:%M:%S.%f+08:00"
t = "2018-10-09T11:22:38.000+08:00"
# date1 = datetime(2017, 8, 23)
# print(mktime(date1.timetuple()))
# print datetime.now()
date = datetime.fromtimestamp(1547087998.500)
date2 = datetime.fromtimestamp(1547174400.286)
print(date)
print(date2)



