# Ambient_Temperature_Logger.py
# 10/12/20    Marco A Magana

import time
#import json
import sys
import csv
#import urllib2
import os

from mod_Temperature.ST_Temperature import *

csv.field_size_limit(sys.maxsize)

OUT_FILE ="TA_results_"
OUT_PATH = "/home/Documents/Share/EDT_AccessCTRL/"
INTERVAL = 300 #seconds (5 min) between polls
WRITE_FILE = True

def retrieve_data(request_string):
        """ Question Melexis Ambient Temperature
        """

        try:
                ta = round(ST_Temperature.GetAmbientTemperature(),1)
        except:
                print("Sensor unreachable. Retrying on next iteration...")
                return {}

def write_file(file, lines):
        """ Write given lines to given file
        """

        time_string = time.strftime("%H:%M:%S", time.localtime())
        for line in lines:
                try:
                        with open(file, "a") as f:
                            f.write("{0},{1}\n".format(time_string,line))
                        #print line
                except:
                        print("WARNING: Failed writing line to file; '{0}'".format(line))


def parse_results(result):
        """ Parse results from Hue API into one CSV line per Hue measurement.
            Returns list of CSV lines
        """
        results_parsed = []

        #Ambient Temperature
        device_line = "{0}".format(device_data)
        results_parsed.append(device_line)
        return results_parsed

# Main loop
while True:
        ta = round(ST_Temperature.GetAmbientTemperature(),1)
        #result_parsed = ""
        result_parsed = parse_results(ta)

        # Write to CSV
        if WRITE_FILE:
                today_date = time.strftime("%Y-%m-%d", time.localtime())
                #time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                out_daily_file = "{0}{1}{2}.csv".format(OUT_PATH, OUT_FILE, today_date)
                #print(out_daily_file)
                write_file(out_daily_file, result_parsed)

        # Finished
        print( "{0} Wrote results for {1} line(s) to {2}{3}.csv. Continuing...".format(time.strftime("%H:%M:%S", time.localtime()), len(result_parsed), OUT_FILE, today_date))

        # Sleep, continue
        time.sleep(INTERVAL)

