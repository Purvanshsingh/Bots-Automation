import MongoConnection
import pandas as pd
import os
from datetime import datetime, timezone
import logger


class HandleData:
    def __init__(self,records):
        self.logger_object = logger.App_Logger()
        self.db_client = MongoConnection.App_mongo_connect()
        self.records = records

    def load_ta_from_db(self, interval, input_datetime,abs_path):
        print("Fetching Data from DataBase Please Wait...")
        try:
            self.data_from_db = self.db_client.get_report_by_time(interval, input_datetime)
            self.data = pd.DataFrame(self.data_from_db["data"])
            #self.data = pd.json_normalize(self.data_from_db)
            output = self.data
            # print(output)
            print("\nExporting loaded data as CSV.")
            # Exporting loaded data as CSV (for debug).

            file_name = "loaded_data_" + interval + "_" + \
                        datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".csv"  # conver this to UTC too?

            file = os.path.join(abs_path, "Ta_files", file_name)
            if self.records:
                output.to_csv(file)
                print("File Saved in Data\\", file_name)

            print("*" * 40)
            return self.data
        except Exception as error:
            print("Error occurred while loading the file.")
            print(error)
