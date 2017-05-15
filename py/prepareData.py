# -*- coding: utf-8 -*-

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


    def read_accelerometer_data(self):
        """
        :return: x,y,z, accelerometer time tags, activity, accelerometer data.
        """

        data = pd.read_csv(self.accelero_file)
        # id = data["ID"]
        x = data["X"]
        y = data["Y"]
        z = data["Z"]
        xyz = data["XYZ"]
        time = data["Time"]
        activity = data["Activity"]
        activity2 = data["Activity2"]

        # New ID field
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
        magNoG, mag = PrepareData.mean_gravity(x, y, z)
        data["magNoG"] = magNoG

        # Magnitude
        data["mag"] = mag

        # Converted activity
        activity_num = PrepareData.convert_activity_accelero(activity)
        data["TRUE ACTIVITY NUM"] = activity_num

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
        activity2 = data["ACTIVITY2"]

        # New ID field
        id = [index for index in range(len(data))]
        data["ID"] = id

        # Convert m/s to km/h
        speed = [speed * 3.6 for speed in speed]
        data["SPEED"] = speed

        # Readable time
        readable_time = []
        for unix in time:
            # String for conversion to geojson
            readable_time.append(str(datetime.datetime.fromtimestamp(unix)))
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

        # Converted activity
        activity_num = PrepareData.convert_activity_geo(activity)
        data["TRUE ACTIVITY NUM"] = activity_num

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
            angle.append(abs(heading[counter]-heading[counter+1]))
        angle.append(0)
        return angle

    @staticmethod
    def mean_gravity(x, y, z):
        """
        Compute magnitude, mean magnitude, and magniitude - mean magnitude
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

        return magNoG, mag

    @staticmethod
    def convert_activity_geo(activity_geo):
        stationary = 1
        walking = 2
        running = 3
        cycling = 4
        car = 5
        public_transport = 6
        unknown = 10

        stationary_list = [" ro ", " garderobe, ", "inne", "inne "]
        walking_list = [" aktivitet ", " sktivitet ", " gar ", " gar, ", "gar", " ute, ", " trapper, ", " ute ", "ute","tf", "tf ", " tf ", " tf", "tf,"]
        running_list = [" tredemolle "]
        cycling_list = []
        car_list = [" bil "]
        public_transport_list = [" t-bane ", " buss ", " tog ", " tog, ", "tog"]
        # TODO: Unknown?, skitur? rema? hjemme? tf?

        activity_geo_num = []
        for activity in activity_geo:
            if activity in stationary_list:
                activity_geo_num.append(stationary)
            elif activity in walking_list:
                activity_geo_num.append(walking)
            elif activity in running_list:
                activity_geo_num.append(running)
            elif activity in cycling_list:
                activity_geo_num.append(cycling)
            elif activity in car_list:
                activity_geo_num.append(car)
            elif activity in public_transport_list:
                activity_geo_num.append(public_transport)
            else:
                activity_geo_num.append(unknown)

        return activity_geo_num
    @staticmethod
    def convert_activity_accelero(activity_accelero):
        stationary = 1
        walking = 2
        running = 3
        cycling = 4
        car = 5
        public_transport = 6
        unknown = 10

        stationary_list = [" ro ", " garderobe, ", "inne", "inne "]
        walking_list = [" aktivitet ", " sktivitet ", " gar ", " gar, ", "gar", " ute, ", " trapper, ", " ute ", "ute", "tf", "tf ", " tf ", " tf", "tf,"]
        running_list = [" tredemolle "]
        cycling_list = []
        car_list = [" bil "]
        public_transport_list = [" t-bane ", " buss ", " tog ", " tog, ", "tog"]
        # TODO: Unknown?, skitur? rema? hjemme? tf?

        activity_accelero_num = []
        for activity in activity_accelero:
            if activity in stationary_list:
                activity_accelero_num.append(stationary)
            elif activity in walking_list:
                activity_accelero_num.append(walking)
            elif activity in running_list:
                activity_accelero_num.append(running)
            elif activity in cycling_list:
                activity_accelero_num.append(cycling)
            elif activity in car_list:
                activity_accelero_num.append(car)
            elif activity in public_transport_list:
                activity_accelero_num.append(public_transport)
            else:
                activity_accelero_num.append(unknown)

        return activity_accelero_num

    def calibration(self, xyz):
        """

        :param xyz: sqrt(x**2 + y**2 + z**2) - g
        :return: average of xyz
        """
        return sum(xyz)/len(xyz)


if __name__ == '__main__':
    pass
