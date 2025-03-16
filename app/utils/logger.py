import csv
import time
import datetime

# For GCS logger, just record every single value received

class Logger():
    def __init__(self):
        self.csvfile = open('logs/{date:%Y_%m_%d_%H_%M_%S}.csv'.format(date=datetime.datetime.now()), 'w', newline='')
        self.csvwriter = csv.writer(self.csvfile, delimiter=',')
        self.header_written = False
        self.start_time = time.time()
    
    def write_log(self, flight_data):
        if not self.header_written:
            self.csvwriter.writerow(("time",) + flight_data.field_names)
            self.header_written = True
        self.csvwriter.writerow([time.time() - self.start_time] + list(flight_data.data))