#!coding=utf-8
import threading
from queue import Queue
from pymongo import MongoClient
from datetime import datetime

# username = 'aduser2'
# password = 'HFtef9Jcc%8EheGt'
# host = '192.168.8.21:27701'
# user = "mongodb://%s:%s@%s" % (username, quote_plus(passwd), host)


class KgiParser:
    def __init__(self):
        self.queue = Queue()  # store msg body
        self.db = MongoClient('localhost')
        self.live = True
        self.dead = 0
        self.pool = []
        for i in range(100):
            self.queue.put(i)

    def store_origin(self, m_data):
        stick = self.db.jy_data.ticks
        data_store = {}
        for d in m_data.header:
            data_store[d] = m_data.header[d]
        for d in m_data.body:
            if d == '40' or d == '50':
                continue
            data_store[d] = m_data.body[d]
        try:
            stick.insert_one(data_store)
        except Exception as err:
            print(err, data_store)
            stick.insert({"error msg": str(err), "content": str(data_store)})

    # label = {'code':'1', "Bid Price":'2',"Bid Quantity":'3',"Ask Price":'4',"Ask Quantity":'5','time':'6'}
    def store_tick(self, m_data):
        if (m_data.header['TRANSMISSION-CODE'], m_data.header['MESSAGE-KIND']) == ('06', '01'):
            stick = self.db.kgi_data["kgi_tick"]
            if len(m_data.body['37']) == 10:
                tick1 = {"1": m_data.body['31'], '2': m_data.body['37'][0][0], '3': m_data.body['37'][0][1],
                         '4': m_data.body['37'][5][0], '5': m_data.body['37'][5][1], "6": m_data.body['32']}
                stick.insert_one(tick1)

            elif len(m_data.body['37']) == 11:
                tick2 = {"1": m_data.body['31'], '2': m_data.body['37'][1][0], '3': m_data.body['37'][1][1],
                         '4': m_data.body['37'][6][0], '5': m_data.body['37'][6][1], "6": m_data.body['32']}
                stick.insert_one(tick2)
        else:
            pass

    # def get_level2(self, m_data):
    #     return m_data['37']

    def parse_body(self):
        print(threading.current_thread().getName())
        # self.join_thread()

    def start(self):
        self.start_thread()
        print("main thread done")

    def start_thread(self):
        for i in range(10):
            self.pool.append(threading.Thread(target=self.parse_body, name="thread" + str(i)))
        [t.start() for t in self.pool]

    def join_thread(self):
        [t.join() for t in self.pool]


if __name__ == "__main__":
    kgi = KgiParser()
    kgi.start()
