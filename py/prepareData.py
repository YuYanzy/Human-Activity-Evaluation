# -*- coding: utf-8 -*-

import csv
import pandas as pd
from shapely.geometry import Point

__author__ = 'eirikaa'


class PrepareData:
    """

    """
    def __init__(self, geo_file, accelero_file, diff_range):
        """

        :param geo_file:
        :param accelero_file:
        :param diff_range:
        """

        self.geo_file = geo_file
        self.accelero_file = accelero_file
        self.diff_range = diff_range

    def readcsv(self):
        """
        Use readcsv2
        """
        x = []
        y = []
        z = []
        xyz = []
        time = []
        activity = []

        csvfile = open(self.geo_file, "r")
        csv_reader = csv.reader(csvfile, delimiter=",")
        for row in csv_reader:
            if row[0] == "ID":
                pass
            elif not(float(row[1]) == 0.0 and float(row[2]) == 0.0 and float(row[3]) == 0.0):
                x.append(float(row[1]))
                y.append(float(row[2]))
                z.append(float(row[3]))
                xyz.append(float(row[4]))
                time.append(float(row[5]))
                activity.append(row[6])

        return x, y, z, xyz, time, activity

    def read_accelerometer_data(self):

        data = pd.read_csv(self.accelero_file)
        id = data["ID"]
        x = data["X"]
        y = data["Y"]
        z = data["Z"]
        xyz = data["XYZ"]
        time =data["Time"]
        activity = data["Activity"]
        activity2 = data["Activity2"]
        
        return x, y, z, xyz, time, activity, activity2, data

    def read_geodata(self):

        data = pd.read_csv(self.geo_file)
        id = data["ID"]
        lat = data["LAT"]
        lon = data["LON"]
        speed = data["SPEED"]
        accuracy = data["ACCURACY"]
        altitude = data["ALTITUDE"]
        heading = data["HEADING"]
        time = data["TIME"]
        activity = data["ACTIVITY"]
        activity2 =data["ACTIVITY2"]

        return lat, lon, speed, accuracy, altitude, heading, time, activity, activity2, data

    def calibration(self, xyz):

        return sum(xyz)/len(xyz)


    def diff_maxmin(self, x, y, z, xyz):
        """

        :param x:
        :param y:
        :param z:
        :param xyz:
        :return:
        """
        diff_xyz = []

        for value in range(0, len(xyz)-self.diff_range, self.diff_range):
            diff_xyz.append((abs(max(xyz[value:value+self.diff_range])-min(xyz[value:value+self.diff_range]))))
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
            diff_xyz.append((max(abs(xyz[value:value + self.diff_range])))- ((sum(xyz[value:value + self.diff_range]))/self.diff_range))
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
                print (i)
            diff_xyz_time.append([((max(abs(xyz[value:value + self.diff_range])))- ((sum(xyz[value:value + self.diff_range]))/self.diff_range)),time[i]])

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
                    j +=1
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
            diff_class.append([1,0])

        return diff_class

    # TODO: Some interpolation is nesecarry

if __name__ == '__main__':
    pass