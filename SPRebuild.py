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
    my_filter = {"$and": [{"Timestamp": {"$gte": start_time}},
                          {"Timestamp": {"$lte": end_time}}]}
    missing_document = 0
    total_document = 0
    new_document = 0
    print("The transfer of %s begin" % transfer_date)
    for result in old_collection.find(my_filter).batch_size(10000):
        total_document += 1
        if "t" in result:
            matched_count = tick.count_documents({"$and": [{"code": result["code"]},
                                                           {"t": result["t"]}]})
            if matched_count == 0:
                tick.insert_one(result)
                new_document += 1
        else:
            missing_document += 1
    print("The number of total document is %d" % total_document)
    print("The number of missing document is %d" % missing_document)
    print("The number of new document is %d" % new_document)
    print("The transfer is end")


if __name__ == "__main__":
    start_date = datetime(2018, 7, 11)
    end_date = datetime(2018, 10, 9)
    for i in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=i)
        sp_rebuild(date.strftime("%Y-%m-%d"))
