# coding:utf-8
from pymongo import MongoClient

myClient = MongoClient('192.168.8.21', 27701)  # 参数是IP和端口
my_db = myClient.admin  # 此行以及下行基本可以照抄
my_db.authenticate("aduser2", "HFtef9Jcc%8EheGt")   # 参数为用户名和密码
database = myClient["bloomberg"]  # 选中一个数据库，如果没有则直接创建
collection = database.tick
result = collection.find({"BID_UPDATE_STAMP_RT": {"$exists": True}}).skip(73000)
print result.count()
