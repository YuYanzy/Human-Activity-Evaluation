# -*- coding: utf-8 -*-

import csv
import pandas as pd

__author__ = 'eirikaa'


class PrepareData:
    """

    """
    def __init__(self, geo_file, accelero_file):
        """

        :param geo_file:
        :param accelero_file:
        :param diff_range:
        """

        self.geo_file = geo_file
        self.accelero_file = accelero_file

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


if __name__ == '__main__':
    pass