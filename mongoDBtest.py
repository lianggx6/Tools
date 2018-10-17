# coding:utf-8
import pymongo

myClient = pymongo.MongoClient('192.168.8.21', 27701)  # 参数是IP和端口
my_db = myClient.admin  # 此行以及下行基本可以照抄
my_db.authenticate("aduser2", "HFtef9Jcc%8EheGt")   # 参数为用户名和密码
database = myClient["kgi_test"]  # 选中一个数据库，如果没有则直接创建
collect = database.list_collection_names()
# for c in collect:
#     database[c].drop()
