# -*- coding: utf-8 -*-

from prepareData import PrepareData
import pandas as pd
import csv

__author__ = 'eirikaa'


class Process:
    def __init__(self):
        pass

    @staticmethod
    def is_subway(file):
        user_data = []


        for i in range(len(file)):
            lon = file[i][2]
            lat = file[i][1]
            speed = float(file[i][4]) * 3.6  # km/h
            # print (read_API(lat, lon))
            user_data.append(read_API_tog(lat, lon))
            if (user_data[i][1] == True) or (user_data[i - 1][1] == True) or (user_data[i - 2][1] == True) or (
                user_data[i - 3][1] == True):
                print('woha', user_data[i])
                if speed >= 20:
                    csv_writer.writerow([i, lat, lon, speed, 'subway', 'driving'])
                else:
                    csv_writer.writerow([i, lat, lon, speed, 'subway', 'not_driving'])

            else:
                if speed >= 20:
                    print('booo', user_data[i])
                    csv_writer.writerow([i, lat, lon, speed, 'not_subway', 'driving'])
                else:
                    csv_writer.writerow([i, lat, lon, speed, 'not_subway', 'not_driving'])


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
    def test2(data_geo):
        kmh = 1.609344
        csv_out = "data/processed/output.csv"
        csvfile_output = open(csv_out, 'w')
        csv_writer = csv.writer(csvfile_output)
        csv_writer.writerow(['Index', 'lat', 'lon', 'speed', 'subway', 'driving'])

        for i, speed in enumerate (data_geo["SPEED"]):
            if speed * kmh >= 10:
                csv_writer.writerow([i, data_geo["LAT"][i], data_geo["LON"][i], data_geo["SPEED"][i] * kmh, "Driving"])
            elif speed * kmh < 1.5:
                csv_writer.writerow([i, data_geo["LAT"][i], data_geo["LON"][i], data_geo["SPEED"][i] * kmh, "Stationary"])
            else:
                csv_writer.writerow([i, data_geo["LAT"][i], data_geo["LON"][i], data_geo["SPEED"][i] * kmh, "Walking"])
        csvfile_output.close()
    def diff(self):
        # TODO: move diff and classify here?
        pass

if __name__ == "__main__":
    ana = PrepareData(geo_file='data/log/02_12_2_geo.csv', accelero_file='data/log/02_12_2_accelero.csv', diff_range=2)
    x, y, z, xyz, time, activity, activity2, data_accelero = ana.read_accelerometer_data()
    lat, lon, speed, accuracy, altitude, heading, time, activity, activity2, data_geo = ana.read_geodata()
    diff_xyz = ana.diff(x, y, z, xyz)
    diff_class = ana.classify(diff_xyz, xyz)

    Process.test2(data_geo)
    print (data_geo["SPEED"][1])
    print (type(data_geo))
    # print(data_geo["SPEED" > 10])
    # print (speed)