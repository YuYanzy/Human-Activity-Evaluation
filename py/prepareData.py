# -*- coding: utf-8 -*-

import csv
import pandas as pd
import datetime
import math

__author__ = 'eirikaa'


class PrepareData:
    """
        This class will prepare data from the CSV files that correspons to
        accelerometer and geolocation data.
    """
    def __init__(self, geo_file, accelero_file):
        """

        :param geo_file: CSV file, geolocation data.
        :param accelero_file: CSV file, accelerometer data.
        """

        self.geo_file = geo_file
        self.accelero_file = accelero_file

    def readcsv(self):
        """
        This method is inactive, use read_accelerometer_data and read_geodata.
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
        """
        :return: x,y,z, accelerometer time tags, activity, accelerometer data.
        """

        data = pd.read_csv(self.accelero_file)
        #id = data["ID"]
        x = data["X"]
        y = data["Y"]
        z = data["Z"]
        xyz = data["XYZ"]
        time =data["Time"]
        activity = data["Activity"]
        activity2 = data["Activity2"]

        #TODO: if x and y and z = 0, not necesarry anymore?
        # TODO: xyz - mean, instead of xyz - g
        #New ID field
        id = [index for index in range(len(data))]
        data['ID'] = id

        # Readable time
        readable_time = []
        for utc in time:
            readable_time.append(datetime.datetime.fromtimestamp(utc))
        data["HUMAN TIME"] = readable_time

        # Time diff
        time_diff = []
        for counter in range(len(time) - 1):
            time_diff.append(time[counter + 1] - time[counter])
        time_diff.append(0)
        data["TIME DIFF"] = time_diff

        # Subtract mean magnitude instead of g = 9.81
        magNoG = PrepareData.mean_gravity(x, y, z)
        data["magNoG"] = magNoG

        return x, y, z, xyz, time, readable_time, activity, activity2, data

    def read_geodata(self):
        """
        :return: lat, lon, speed, accuracy, altitude, heading,
        geolocation time tags, activity, geolocation data.
        """

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

        #New ID field
        id = [index for index in range(len(data))]
        data["ID"] = id

        # Convert m/s to km/h
        speed = [speed * 3.6 for speed in speed]
        data["SPEED"] = speed

        # Readable time
        readable_time = []
        for utc in time:
            # String for conversion to geojson
            readable_time.append(str(datetime.datetime.fromtimestamp(utc)))
        data["HUMAN TIME"] = readable_time

        # Time diff
        time_diff = []
        for counter in range(len(time)-1):
            time_diff.append(time[counter+1]-time[counter])
        time_diff.append(0)
        data["TIME DIFF"] = time_diff

        # Angle
        angle = PrepareData.compute_angle(heading)
        data["ANGLE"] = angle

        return lat, lon, speed, accuracy, altitude, heading, time, readable_time, activity, activity2, data

    @staticmethod
    def compute_angle(heading):
        """
        Compute angle between points

        :param heading:
        :return:
        """

        angle = []
        for counter in range(len(heading)-1):
            angle.append(heading[counter]-heading[counter+1])
        angle.append(0)
        return angle

    @staticmethod
    def mean_gravity(x, y, z):
        """
        Compute mean gravity
        :param x:
        :param y:
        :param z:
        :return:
        """

        mag = []
        for counter in range(len(x)):
            mag.append((math.sqrt((x[counter]) ** 2 + (y[counter]) ** 2 + (z[counter]) ** 2)))
        mean = sum(mag)/len(mag)
        magNoG = [i-mean for i in mag]

        return magNoG

    def calibration(self, xyz):
        """

        :param xyz: sqrt(x**2 + y**2 + z**2) - g
        :return: average of xyz
        """
        return sum(xyz)/len(xyz)


if __name__ == '__main__':
    pass