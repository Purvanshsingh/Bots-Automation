from pymongo import MongoClient
from functools import reduce
from datetime import datetime, timezone, timedelta


class App_mongo_connect:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://dbReader:kriE0s9iWeYnRGD1@cluster2.8bri5.mongodb.net/test?retryWrites=true&w=majority")

        self.db = self.client.ccMain

    def get_report_by_time(self, interval, created_for_time):
        db_result = self.db.market_TA_reports_binance.find_one(
            {"interval": interval, "created_for_time": created_for_time},{'_id': False})
        if(db_result == None):
            print("FAILED: Loading data report from "+str(created_for_time))
            return False

        result = dict(db_result)
        print("SUCCESS: Loading data report from " +
              result['hr_created_for_time'] + "("+str(created_for_time)+")")
        return result

    def __del__(self):
        self.client.close()
