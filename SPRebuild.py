# coding:utf-8
from datetime import datetime, timedelta
from pymongo import MongoClient


def sp_rebuild(transfer_date):
    my_client = MongoClient('113.108.181.148', 27701)  # 参数是IP和端口
    my_db = my_client.admin  # 此行以及下行基本可以照抄
    my_db.authenticate("aduser2", "HFtef9Jcc%8EheGt")  # 参数为用户名和密码
    sp_trader = my_client.sp_trader  # 选中一个数据库，如果没有则直接创建
    tick = sp_trader.tick
    old_database = my_client.jy_data
    old_collection = old_database.sp
    start_time = datetime.strptime(transfer_date, "%Y-%m-%d").timestamp()
    end_time = (datetime.strptime(transfer_date, "%Y-%m-%d") + timedelta(days=1)).timestamp()
    my_filter = {"$and": [{"t": {"$gte": start_time}},
                          {"t": {"$lte": end_time}}]}
    print(str(datetime.now()) + " The transfer of %s begin" % transfer_date)
    document_buffer = []
    for result in old_collection.find(my_filter, {"_id": 0}).batch_size(10000):
        if result not in document_buffer:
            if len(document_buffer) >= 10:
                tick.insert_one(document_buffer.pop(0))
            document_buffer.append(result)
    for buf in document_buffer:
        tick.insert_one(buf)
    print(str(datetime.now()) + " The transfer is end")


if __name__ == "__main__":
    start_date = datetime(2018, 10, 15)
    end_date = datetime(2018, 10, 16)
    for i in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=i)
        sp_rebuild(date.strftime("%Y-%m-%d"))
