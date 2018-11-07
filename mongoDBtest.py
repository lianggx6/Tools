# coding:utf-8
from datetime import datetime

import pymongo

myClient = pymongo.MongoClient('192.168.8.21', 27701)  # 参数是IP和端口
my_db = myClient.admin  # 此行以及下行基本可以照抄
my_db.authenticate("aduser2", "HFtef9Jcc%8EheGt")   # 参数为用户名和密码
database = myClient["KGI"]  # 选中一个数据库，如果没有则直接创建
collection = database.future_tick
newcoll = myClient["jy_data"].KGI_future
for i in range(9, 12):
    date = datetime(2018, 8, i).strftime("%Y-%m-%d")
    print(str(datetime.now()) + " start the " + date)
    for result in collection.find({"DATE": date}).batch_size(10000):
        newcoll.insert_one(result)
    print(str(datetime.now()) + " end the " + date)
