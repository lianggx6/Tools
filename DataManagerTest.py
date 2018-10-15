import pymongo
import pytz
from datetime import timedelta, datetime


class DataManager:
    def __init__(self, host=None, port=None, user=None, password=None):
        self.client = pymongo.MongoClient(host, port)
        admins = self.client.admin
        admins.authenticate(user, password)

    def transfer_history_data(self, source_database, source_collection,
                              load_database, start_time, end_time):
        start_date = datetime.strptime(start_time, "%Y-%m-%d")
        end_date = datetime.strptime(end_time, "%Y-%m-%d") + timedelta(days=1)
        source_database = self.client[source_database]
        source_collection = source_database[source_collection]
        load_database = self.client[load_database]
        if source_database.name == "jy_data" and source_collection.name == "sp":
            start_timestamp = start_date.timestamp()
            end_timestamp = end_date.timestamp()
            my_filter = {"$and": [{"Timestamp": {"$gte": start_timestamp}},
                                  {"Timestamp": {"$lte": end_timestamp}}]}
            self.transfer_from_sp(source_collection, load_database, my_filter)
        if source_database.name == "bloomberg" and source_collection.name == "tick":
            datetime_format = "%Y-%m-%dT%H:%M:%S.000+08:00"
            start_time = start_date.strftime(datetime_format)
            end_time = end_date.strftime(datetime_format)
            my_filter = {"$or": [{"$and": [{"BID_UPDATE_STAMP_RT": {"$gte": start_time}},
                                           {"BID_UPDATE_STAMP_RT": {"$lte": end_time}}]},
                                 {"$and": [{"ASK_UPDATE_STAMP_RT": {"$gte": start_time}},
                                           {"ASK_UPDATE_STAMP_RT": {"$lte": end_time}}]}]}
            self.transfer_from_bloomberg(source_collection, load_database, my_filter)

    def transfer_data(self, source_database, source_collection,
                      load_database):
        source_database = self.client[source_database]
        source_collection = source_database[source_collection]
        load_database = self.client[load_database]
        if source_database.name == "jy_data" and source_collection.name == "ticks":
            self.transfer_from_ticks(source_collection, load_database)
        if source_database.name == "jy_data" and source_collection.name == "sp":
            self.transfer_from_sp(source_collection, load_database, {})
        if source_database.name == "bloomberg" and source_collection.name == "tick":
            self.transfer_from_bloomberg(source_collection, load_database, {})

    def transfer_from_kgi(self):

        pass

    @staticmethod
    def transfer_from_bloomberg(source_collection,
                                load_database, my_filter):
        my_select = {"_id": 0, "code": 1, "BID": 1, "BID_SIZE": 1, "BID_UPDATE_STAMP_RT": 1,
                     "ASK": 1, "ASK_SIZE": 1, "ASK_UPDATE_STAMP_RT": 1}
        for result in source_collection.find(my_filter, my_select).batch_size(10000):
            security = result["code"].zfill(15)[0:5] + "_HKEX" \
                if "HK" in result["code"] else result["code"][0:6] + "_SHSE" \
                if result["code"][0:2] == "60" or result["code"][0:2] == "90" \
                else result["code"][0:6] + "_SZSE"
            datetime_format = "%Y-%m-%dT%H:%M:%S.%f+08:00"
            document = {
                "Security": security,
                "Datetime": datetime.strptime(result["BID_UPDATE_STAMP_RT"], datetime_format),
                "BID_price": result["BID"],
                "BID_volume": result["BID_SIZE"]
            } if "BID" in result \
                else {
                "Security": security,
                "Datetime": datetime.strptime(result["ASK_UPDATE_STAMP_RT"], datetime_format),
                "ASK_price": result["ASK"],
                "ASK_volume": result["ASK_SIZE"]
            }
            document["Datetime"] = document["Datetime"].astimezone(pytz.timezone("UTC"))
            document["timestamp"] = document["Datetime"].timestamp()
            load_collection = load_database[document["Security"]]
            update_res = load_collection.update_one({"$and": [{"Security": security},
                                                              {"Datetime": document["Datetime"]}]},
                                                    {"$set": document})
            if update_res.matched_count == 0:
                document.pop("timestamp")
                load_collection.insert_one(document)

    @staticmethod
    def transfer_from_sp(source_collection,
                         load_database, my_filter):
        print("start")
        my_select = {"_id": 0, "code": 1, "Bid": 1, "BidQty": 1,
                     "Ask": 1, "AskQty": 1, "Timestamp": 1}
        for result in source_collection.find(my_filter, my_select).batch_size(10000):
            date = datetime.fromtimestamp(result["Timestamp"]).astimezone(pytz.timezone("UTC"))
            document = {
                "Security": result["code"],
                "Datetime": date,
                "BID_price": result["Bid"][0],
                "BID_volume": result["BidQty"][0],
                "ASK_price": result["Ask"][0],
                "ASK_volume": result["AskQty"][0],
                "timestamp": result["Timestamp"]
            }
            load_collection = load_database[document["Security"]]
            load_collection.insert_one(document)

    @staticmethod
    def transfer_from_ticks(source_collection,
                            load_database):
        my_filter = {'2': {'$ne': "T"}}
        my_select = {"_id": 0, "c": 1, "d": 1, "t": 1,
                     "3": 1, "6": 1, "8": 1, "11": 1}
        for result in source_collection.find(my_filter, my_select).batch_size(10000):
            cu = load_database[result['c'] + result['d']]
            security = result['c'] + result['d'] + "_SHFE"
            document = {
                "Security": security,
                "Datetime": result["t"],
                "BID_price": result["3"],
                "BID_volume": result["6"],
                "ASK_price": result["8"],
                "ASK_volume": result["11"],
            }
            document["Datetime"] = (document["Datetime"] + timedelta(hours=12)).astimezone(pytz.timezone("UTC"))
            document["timestamp"] = document["Datetime"].timestamp()
            cu.insert_one(document)


if __name__ == "__main__":
    data_manger = DataManager("113.108.181.148", 27701, "aduser2", "HFtef9Jcc%8EheGt")
    # data_manger.transfer_data("jy_data", "ticks", "stock_tick")
    data_manger.transfer_history_data("bloomberg", "tick", "stock_tick", "2018-09-27", "2018-09-27")
