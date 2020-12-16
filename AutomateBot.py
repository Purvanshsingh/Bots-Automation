"""
1. load ta report from DB
2. sepreate all "to_ccy" wth USDT
3. check if rsi_14 status is low open dear else close the deal.
"""
import argparse
import os
import logger
import HandleData
import sys
from datetime import datetime, timezone, time

class AutomateBot:
    def __init__(self):
        parser = argparse.ArgumentParser()

        # Arguments
        parser.add_argument('--interval', type=str, default='1h',
                            help='1h / 4h / 1d / 15m, default - 1h')
        parser.add_argument('--input_datetime', type=str,
                            default='', help='Default - ""')
        parser.add_argument('--log_level', type=str, default='default',
                            help='default / critical, default - "default"')
        parser.add_argument('--local_file', type=str, default='',
                            help='Default - False')
        parser.add_argument('--records', type=str, default="False",
                            help='Default - False')
        args = vars(parser.parse_args())
        # clearing sys.argv to prevent passing them to other files
        sys.argv = [sys.argv[0]]

        print("Input Parameters are:")
        print(args)

        self.interval = args['interval']
        self.input_datetime = args['input_datetime']
        self.log_level = args['log_level']
        self.local_file = args['local_file']
        self.records = eval(args['records'])
        self.data = None

        # check arguments - exit with error if they are malformed

        self.abs_path = os.path.dirname(os.path.abspath(__file__))

        # logs (if needed)
        log_path = os.path.join(self.abs_path, "Logs", "log.txt")
        dev_log_path = os.path.join(self.abs_path, "Logs", "developer_log.txt")
        if self.local_file:
            if os.path.isfile(os.path.join(self.abs_path, "Local_files", self.local_file)):
                self.local_file_path = os.path.join(self.abs_path, "Local_files", self.local_file)
            else:
                print("Local_file does not exist!")
                print("Terminated!")
                os.exit(-1)

        self.log_file = open(log_path, "a+")
        self.developer_log_file = open(dev_log_path, "a+")
        self.logger_object = logger.App_Logger()

        self.log_info = {
            'abs_path': self.abs_path,
            'log_file': self.log_file,
            'logger_object': self.logger_object,
            'developer_log_file': self.developer_log_file
        }

        # Converting datetime to string format

        self.datetime_string_format = "%d_%m_%Y_%H_00_00"

        if self.input_datetime == '':
            # stripping hours & add utc
            time_now = datetime.now(timezone.utc).strftime(
                self.datetime_string_format + "%z")
            self.input_datetime = datetime.strptime(
                time_now, "%d_%m_%Y_%H_%M_%S%z")
            print("Using default datetime " +
                  self.input_datetime.strftime("%Y-%m-%d %H:%M:%S%z"))
        else:
            # we use only UTC time as input
            self.input_datetime = datetime.strptime(self.input_datetime, "%d_%m_%Y_%H_%M_%S").replace(
                tzinfo=timezone.utc)
            print("Using input datetime " +
                  self.input_datetime.strftime("%Y-%m-%d %H:%M:%S%z"))

    def get_ta_data(self):
        if self.local_file:
            self.data = pd.read_csv(self.local_file_path)
        else:
            # let's calculate proper timestamp here
            timestamp_in_ms = self.input_datetime.timestamp() * 1000
            self.data = HandleData.HandleData(self.records).load_ta_from_db(
                self.interval, timestamp_in_ms, self.abs_path)
        print(self.data.head(3))
        print("*" * 40)

if __name__ == "__main__":
    AutomateBot().get_ta_data()