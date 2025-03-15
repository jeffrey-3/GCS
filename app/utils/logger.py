import csv
import time
import datetime

# For GCS logger, just record every single value received

class Logger():
    def __init__(self):
        self.csvfile = open('logs/{date:%Y_%m_%d_%H_%M_%S}.csv'.format(date=datetime.datetime.now()), 'w', newline='')
        self.csvwriter = csv.writer(self.csvfile, delimiter=',')
        self.csvwriter.writerow(["time", "roll", "pitch", "heading"])
    
    def write_log(self, flight_data):
        self.csvwriter.writerow([time.time(),
                                 flight_data.roll, 
                                 flight_data.pitch, 
                                 flight_data.heading, 
                                 flight_data.altitude, 
                                 flight_data.speed,
                                 flight_data.lat,
                                 flight_data.lon,
                                 flight_data.mode_id,
                                 flight_data.wp_idx])