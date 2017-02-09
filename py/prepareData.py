# -*- coding: utf-8 -*-

import csv
import pandas as pd
from shapely.geometry import Point

__author__ = 'eirikaa'


class PrepareData:
    """

    """
    def __init__(self, filename):
        """

        :param filename:
        """
        self.filename = filename

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

        csvfile = open(self.filename, "r")
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

        data = pd.read_csv(self.filename)
        id = data["ID"]
        x = data["X"]
        y = data["Y"]
        z = data["Z"]
        xyz = data["XYZ"]
        time =data["Time"]
        activity = data["Activity"]
        activity2 = data["Activity2"]
        
        return x, y, z, xyz, time, activity, activity2

    def read_geodata(self):

        data = pd.read_csv(self.filename)
        id = data["ID"]
        lat = data["LAT"]
        lon = data["LON"]
        accuracy = data["ACCURACY"]
        altitude = data["ALTITUDE"]
        heading = data["HEADING"]
        time = data["TIME"]
        activity = data["ACTIVITY"]
        activity2 =data["ACTIVITY2"]

        return lat, lon, accuracy, altitude, heading, time, activity, activity2, data

    def calibration(self, xyz):

        return sum(xyz)/len(xyz)



    def diff(self, x, y, z, xyz):
        """

        :param x:
        :param y:
        :param z:
        :param xyz:
        :return:
        """
        diff_xyz = []
        diff_range = 10

        for value in range(0, len(xyz)-diff_range, diff_range):
            diff_xyz.append(abs(max(xyz[value:value+diff_range])-min(xyz[value:value+diff_range])))
        return diff_xyz

    def classify(self, diff_xyz):
        """

        :param diff_xyz:
        :return:
        """

        activity_threshold = 3
        hard_activity_threshold = 17
        activity = 40
        hard_activity = 45
        low_activity = -40
        # FIXME: fix this
        diff_class = []
        # TODO: label the diff classes diffenrently
        for diff in diff_xyz:
            if diff >= hard_activity_threshold:
                diff_class.append(hard_activity)
                diff_class.append(hard_activity)
                diff_class.append(hard_activity)
                diff_class.append(hard_activity)
                diff_class.append(hard_activity)
                diff_class.append(hard_activity)
                diff_class.append(hard_activity)
                diff_class.append(hard_activity)
                diff_class.append(hard_activity)
                diff_class.append(hard_activity)

            elif diff >= activity_threshold:
                diff_class.append(activity)
                diff_class.append(activity)
                diff_class.append(activity)
                diff_class.append(activity)
                diff_class.append(activity)
                diff_class.append(activity)
                diff_class.append(activity)
                diff_class.append(activity)
                diff_class.append(activity)
                diff_class.append(activity)

            else:
                diff_class.append(low_activity)
                diff_class.append(low_activity)
                diff_class.append(low_activity)
                diff_class.append(low_activity)
                diff_class.append(low_activity)
                diff_class.append(low_activity)
                diff_class.append(low_activity)
                diff_class.append(low_activity)
                diff_class.append(low_activity)
                diff_class.append(low_activity)

        return diff_class

if __name__ == '__main__':
    pass