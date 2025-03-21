import csv
import time
import datetime

# For GCS logger, just record every single value received

class Logger():
    def __init__(self):
        self.csvfile = open('logs/{date:%Y_%m_%d_%H_%M_%S}.csv'.format(date=datetime.datetime.now()), 'w', newline='')
        self.csvwriter = csv.writer(self.csvfile, delimiter=',')
        self.header_written = False
        self.start_time = 0
    
    def write_log(self, telem_packet):
        if self.start_time == 0:
            self.start_time = time.time()

        if not self.header_written:
            self.csvwriter.writerow(("time",) + telem_packet.field_names)
            self.header_written = True

        data = [1 if value is True else 0 if value is False else value for value in telem_packet.data]

        self.csvwriter.writerow([time.time() - self.start_time] + data)