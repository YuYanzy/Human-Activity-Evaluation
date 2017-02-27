# -*- coding: utf-8 -*-

import pandas as pd
import requests
import json
import math

__author__ = 'eirikaa'


class Classification:
    """
    This class will classify and differentiate data
    """
    def __init__(self, diff_range):
        """

        :param diff_range: The number of elements in the data lists which will make up epochs
        """
        self.diff_range = diff_range

    @staticmethod
    def read_api_train(lat, lon):
        """

        :param lat:
        :param lon:
        :return:
        """

        req = requests.get('http://188.166.168.99/tog/?lon=' + str(lon) + '&lat=' + str(lat))
        req = req.content.decode(req.apparent_encoding)
        req = json.loads(req)
        return req

    @staticmethod
    def read_api_bus(lat, lon):
        """

        :param lat:
        :param lon:
        :return:
        """
        req = requests.get('http://188.166.168.99/buss/?lon=' + str(lon) + '&lat=' + str(lat))
        req = req.content.decode(req.apparent_encoding)
        req = json.loads(req)
        return req

    def diff_maxmin(self, xyz):
        """

        :param xyz:
        :return:
        """
        diff_xyz = []

        for value in range(0, len(xyz) - self.diff_range, self.diff_range):
            diff_xyz.append((abs(max(xyz[value:value + self.diff_range]) - min(xyz[value:value + self.diff_range]))))
        return diff_xyz

    def diff_avg(self, xyz):
        """

        :param xyz:
        :return:
        """
        diff_xyz = []

        for value in range(0, len(xyz) - self.diff_range, self.diff_range):
            diff_xyz.append((max(abs(xyz[value:value + self.diff_range]))) - (
                (sum(xyz[value:value + self.diff_range])) / self.diff_range))
        return diff_xyz

    # TODO: implement method with number of peaks or similar, or summerize the magnitude

    def diff_sum(self, xyz):
        """

        :param xyz:
        :return:
        """
        diff_xyz = []
        sum_xyz = 0
        for value in range(len(xyz)):
            sum_xyz += xyz[value]
            if value % self.diff_range == 0 and value != 0:
                diff_xyz.append(sum_xyz)
                sum_xyz = 0

        return diff_xyz

    def diff_sum_variance(self, xyz):
        """

        :param xyz:
        :return:
        """

        diff_xyz = []
        sum_xyz = 0
        temp_value = []
        variance = []

        for counter in range(len(xyz)):
            sum_xyz += xyz[counter]
            temp_value.append(xyz[counter])
            if counter % self.diff_range == 0 and counter != 0:
                mean = sum_xyz / self.diff_range
                # for i in temp_value:
                variance.append(sum((mean-value)**2 for value in temp_value) / len(temp_value))
                diff_xyz.append(sum_xyz)
                sum_xyz = 0
                temp_value = []

        std = [math.sqrt(var) for var in variance]

        return variance

        # TODO: sum of variance?
        # TODO: implement method to
    def num_steps(self):
        pass
    # TODO: findpeaks

    def differentiate(self, diff_xyz, xyz, time):
        """

        :param diff_xyz:
        :param xyz:
        :param time:
        :return:
        """
        # TODO: Move the diff methods here
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
        for _ in range(a):
            diff_class.append([1, 0])

        return diff_class

    @staticmethod
    def classify_geo_data(diff_class, time_geo, data_accelero, data_geo):
        diff_class_geo_time = []
        time_geo = list(time_geo)

        for i in range(len(data_accelero)):

            accelero_to_geo_time = min(time_geo, key=lambda x: abs(x-diff_class[i][1]))
            diff_class_geo_time.append([diff_class[i][0], accelero_to_geo_time])

        temp_list = []
        temp_diff_list = []
        diff_list = []
        for j in range(1, len(diff_class_geo_time)):        # Diff class_geo_time = [[diff_class, geo time based on closest value from accelero time]]
            temp_time = diff_class_geo_time[j][1]               # Temp time = [geo_time1, geo_time2, ..., geo_time_n]
            if temp_time == diff_class_geo_time[j - 1][1]:      # if geo_time == geo_time - 1
                temp_list.append(diff_class_geo_time[j])            # temp_list = [[diff_class, geo time based on closest value from accelero time]] without
                temp_diff_list.append(diff_class_geo_time[j][0])    # temp_diff_list = [diff classes which coresseponds to time]
                print(temp_diff_list)
            else:
                print('true')
                if len(temp_diff_list) > 0:
                    diff_list.append(max(set(temp_diff_list), key=temp_diff_list.count))  # diff_list =
                else:
                    diff_list.append(1)
                print(diff_list)
                print(len(diff_list))
                temp_list = []
                temp_diff_list = []


        # Remaining values
        a = len(data_geo) - len(diff_list)
        for i in range(a):
            diff_list.append(1)


        data_geo["DIFF CLASS"] = diff_list

        # TODO: move this
        data_geo.to_csv("data/processed/test.csv")

    @staticmethod
    def test(data):
        """
        Inactive
        :param data:
        :return:
        """
        kmh = 3.6
        a = pd.DataFrame()
        for speed in data["SPEED"]:
            if speed * kmh >= 10:
                print("Driving", speed)
            else:
                print("Walking", speed)

            # speed.to_csv(path_or_buf="data/processed/pandacsv.csv", index=True)
        # TODO: learn Pandas


    @staticmethod
    def write_csv(data_geo, diff_class):
        activity = []

        for i in range(len(data_geo)):
            # print((Process.read_API_tog(data_geo["LAT"][i], data_geo["LON"][i])))
            print('hallo')
            if Classification.read_api_train(data_geo["LAT"][i], data_geo["LON"][i])[1]:
                activity.append("Train")
            elif data_geo["SPEED"][i] >= 10:
                activity.append("Driving")
            elif data_geo["SPEED"][i] < 1.5:
                activity.append("Stationary")
            else:
                activity.append("Walking")

        data_geo["Processed Activity"] = activity

    # @staticmethod
    # def write_csv(data_geo, diff_class):
    #     activity = []
    #
    #     for i in range(len(data_geo)):
    #
    #         if Classification.read_api_tog(data_geo["LAT"][i], data_geo["LON"][i])[1] and :
    #             activity.append("Train")
    #         elif data_geo["SPEED"][i] >= 10:
    #             activity.append("Driving")
    #         elif data_geo["SPEED"][i] < 1.5:
    #             activity.append("Stationary")
    #         else:
    #             activity.append("Walking")
    #
    #     data_geo["Processed Activity"] = activity

    @staticmethod
    def smooth_data(data_geo):
        # TODO: try this on raw accelerometer data as well
        for counter in range(len(data_geo)):
            temp_diff_class = data_geo["DIFF CLASS"][counter]
            print(temp_diff_class)

        # TODO: Not sure how to this smart, maybe try to get the classification in diff classes better to start with

if __name__ == "__main__":
    pass



