# coding:utf-8
# from datetime import datetime
from pymongo import MongoClient

myClient = MongoClient('192.168.8.21', 27701)  # 参数是IP和端口
my_db = myClient.admin  # 此行以及下行基本可以照抄
my_db.authenticate("aduser2", "HFtef9Jcc%8EheGt")   # 参数为用户名和密码
database = myClient["ticks_new"]
for collection in database.collection_names():
    if "HKEX" in collection or "SHSE" in collection or \
            "SZSE" in collection or "US" in collection:
        database[collection].drop()
