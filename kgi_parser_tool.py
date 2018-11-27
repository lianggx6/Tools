from datetime import datetime, timedelta
from kgi_parser import KgiParser

if __name__ == "__main__":
    start_date = datetime(2018, 11, 19)
    end_date = datetime(2018, 11, 24)
    for i in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=i)
        kgi = KgiParser(True, date)
        print (str(datetime.now()) + " start the stock parse of " + str(date.date()))
        kgi.start()
        print (str(datetime.now()) + " end the stock parse of " + str(date.date()))
        print (str(datetime.now()) + " start the future parse of " + str(date.date()))
        kgi = KgiParser(False, date)
        kgi.start()
        print (str(datetime.now()) + " end the future parse of " + str(date.date()))
