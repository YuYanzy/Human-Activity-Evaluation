# -*- coding: utf-8 -*-

from prepareData import PrepareData
import pandas as pd
import csv
import requests
import json

__author__ = 'eirikaa'


class Process:
    def __init__(self):
        pass

    @staticmethod
    def read_API_tog(lat, lon):

        req = requests.get('http://188.166.168.99/tog/?lon=' + str(lon) + '&lat=' + str(lat))
        req = req.content.decode(req.apparent_encoding)
        req = json.loads(req)
        return req

    @staticmethod
    def read_API_buss(lat, lon):

        req = requests.get('http://188.166.168.99/buss/?lon=' + str(lon) + '&lat=' + str(lat))
        req = req.content.decode(req.apparent_encoding)
        req = json.loads(req)
        return req



    @staticmethod
    def test(data):
        kmh = 1.609344
        a = pd.DataFrame()
        for speed in data["SPEED"]:
            if speed * kmh >= 10:
                print ("Driving", speed)
            else: print("Walking", speed)

            # speed.to_csv(path_or_buf="data/processed/pandacsv.csv", index=True)
        # TODO: learn Pandas

    @staticmethod
    def test2(data_geo, diff_class):
        kmh = 3.6
        csv_out = "data/processed/output.csv"
        csvfile_output = open(csv_out, 'w')
        csv_writer = csv.writer(csvfile_output)
        csv_writer.writerow(['ID', 'LAT', 'LON', 'SPEED', 'ACTIVITY',])

        for i in range (len(data_geo)):
            # print((Process.read_API_tog(data_geo["LAT"][i], data_geo["LON"][i])))

            if (Process.read_API_tog(data_geo["LAT"][i], data_geo["LON"][i])[1]) == True:
                csv_writer.writerow([i, data_geo["LAT"][i], data_geo["LON"][i], data_geo["SPEED"][i] * kmh, "Train"])
            elif  data_geo["SPEED"][i]* kmh >= 10:
                csv_writer.writerow([i, data_geo["LAT"][i], data_geo["LON"][i], data_geo["SPEED"][i] * kmh, "Driving"])
            elif data_geo["SPEED"][i] * kmh < 1.5:
                csv_writer.writerow([i, data_geo["LAT"][i], data_geo["LON"][i], data_geo["SPEED"][i] * kmh, "Stationary"])
            else:
                csv_writer.writerow([i, data_geo["LAT"][i], data_geo["LON"][i], data_geo["SPEED"][i] * kmh, "Walking"])
        csvfile_output.close()

    def diff(self):
        # TODO: move diff and classify here?
        pass

if __name__ == "__main__":
    ana = PrepareData(geo_file='data/log/02_12_2_geo.csv', accelero_file='data/log/02_12_2_accelero.csv', diff_range=10)
    x, y, z, xyz, time, activity, activity2, data_accelero = ana.read_accelerometer_data()
    lat, lon, speed, accuracy, altitude, heading, time, activity, activity2, data_geo = ana.read_geodata()
    diff_xyz = ana.diff_maxmin(x, y, z, xyz)
    diff_class = ana.classify(diff_xyz, xyz, time)
    print (diff_class)
    Process.test2(data_geo, diff_class)

    # TODO: make geojson lines