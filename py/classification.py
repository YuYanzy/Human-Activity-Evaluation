# -*- coding: utf-8 -*-

from prepareData import PrepareData
import pandas as pd
import csv
import requests
import json

__author__ = 'eirikaa'


class Classification:
    def __init__(self, diff_range):
        self.diff_range = diff_range

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

    def diff_maxmin(self, x, y, z, xyz):
        """

        :param x:
        :param y:
        :param z:
        :param xyz:
        :return:
        """
        diff_xyz = []

        for value in range(0, len(xyz) - self.diff_range, self.diff_range):
            diff_xyz.append((abs(max(xyz[value:value + self.diff_range]) - min(xyz[value:value + self.diff_range]))))
        return diff_xyz

    def diff_avg(self, x, y, z, xyz):
        """

        :param x:
        :param y:
        :param z:
        :param xyz:
        :return:
        """
        diff_xyz = []

        for value in range(0, len(xyz) - self.diff_range, self.diff_range):
            diff_xyz.append((max(abs(xyz[value:value + self.diff_range]))) - (
            (sum(xyz[value:value + self.diff_range])) / self.diff_range))
        return diff_xyz

    def diff_avg2(self, x, y, z, xyz, time):
        """

        :param x:
        :param y:
        :param z:
        :param xyz:
        :return:
        """
        diff_xyz = []
        diff_xyz_time = []
        i = -1
        for value in range(0, len(xyz) - self.diff_range, self.diff_range):
            for j in range(self.diff_range):
                i += 1
                print(i)
            diff_xyz_time.append([((max(abs(xyz[value:value + self.diff_range]))) - (
            (sum(xyz[value:value + self.diff_range])) / self.diff_range)), time[i]])

        return diff_xyz_time, diff_xyz

    def classify(self, diff_xyz, xyz, time):
        """

        :param diff_xyz:
        :return:
        """

        activity_threshold = 2.5
        hard_activity_threshold = 10
        activity = 25
        hard_activity = 30
        low_activity = -15
        diff_class = []
        # TODO: label the diff classes diffenrently

        j = -1
        for diff in diff_xyz:
            if diff >= hard_activity_threshold:
                for i in range(self.diff_range):
                    j += 1
                    # diff_class.append(hard_activity)
                    diff_class.append([hard_activity, time[j]])

            elif diff >= activity_threshold:
                for i in range(self.diff_range):
                    j += 1
                    # diff_class.append(activity)
                    diff_class.append([activity, time[j]])
            else:
                for i in range(self.diff_range):
                    j += 1
                    # diff_class.append(low_activity)
                    diff_class.append([low_activity, time[j]])

        # Remaining values
        a = len(xyz) - len(diff_class)
        for i in range(a):
            diff_class.append([1, 0])

        return diff_class

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
    def write_csv(data_geo, diff_class):
        kmh = 3.6
        csv_out = "data/processed/output.csv"
        csvfile_output = open(csv_out, 'w')
        csv_writer = csv.writer(csvfile_output)
        csv_writer.writerow(['ID', 'LAT', 'LON', 'SPEED', 'ACTIVITY',])

        for i in range (len(data_geo)):
            # print((Process.read_API_tog(data_geo["LAT"][i], data_geo["LON"][i])))

            if (Classification.read_API_tog(data_geo["LAT"][i], data_geo["LON"][i])[1]) == True:
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
    prep = PrepareData(geo_file='data/log/02_12_2_geo.csv', accelero_file='data/log/02_12_2_accelero.csv')
    classification = Classification(diff_range=10)
    x, y, z, xyz, time, activity, activity2, data_accelero = prep.read_accelerometer_data()
    lat, lon, speed, accuracy, altitude, heading, time, activity, activity2, data_geo = prep.read_geodata()

    diff_xyz = classification.diff_maxmin(x, y, z, xyz)
    diff_class = classification.classify(diff_xyz, xyz, time)
    print (diff_class)
    Classification.write_csv(data_geo, diff_class)

    # TODO: make geojson lines