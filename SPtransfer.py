# coding:utf-8
from datetime import datetime, timedelta
from time import mktime

from pymongo import MongoClient


def sp_rebuild(transfer_date):
    my_client = MongoClient('192.168.8.21', 27701)  # 参数是IP和端口
    my_db = my_client.admin  # 此行以及下行基本可以照抄
    my_db.authenticate("aduser2", "HFtef9Jcc%8EheGt")  # 参数为用户名和密码
    tick = my_client.jy_data.SP_Trader
    old_collection = my_client.sp_trader.tick
    start_time = mktime(datetime.strptime(transfer_date, "%Y-%m-%d").timetuple())
    end_time = mktime((datetime.strptime(transfer_date, "%Y-%m-%d") + timedelta(days=1)).timetuple())
    my_filter = {"$and": [{"t": {"$gte": start_time}},
                          {"t": {"$lte": end_time}}]}
    print(str(datetime.now()) + " The transfer of %s begin" % transfer_date)
    for result in old_collection.find(my_filter, {"_id": 0}).batch_size(10000):
                tick.insert_one(result)
    print(str(datetime.now()) + " The transfer is end")


if __name__ == "__main__":
    start_date = datetime(2018, 9, 7)
    end_date = datetime(2018, 11, 5)
    for i in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=i)
        sp_rebuild(date.strftime("%Y-%m-%d"))
