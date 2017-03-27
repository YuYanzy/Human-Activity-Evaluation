# -*- coding: utf-8 -*-

import requests
import json
import math
import operator

__author__ = 'eirikaa'


class Classification:
    """
    This class will classify and differentiate data
    """
    def __init__(self, diff_range, data_geo):
        """

        :param diff_range: The number of elements in the data lists which will make up epochs
        """
        self.diff_range = diff_range
        self.data_geo = data_geo
        # TODO: data_geo

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

    def num_steps(self):
        pass
    # TODO: findpeaks

    def differentiate(self, diff_xyz, xyz, time, activity_threshold=2.5, hard_activity_threshold=10):
        """

        :param diff_xyz:
        :param xyz:
        :param time:
        :param activity_threshold:
        :param hard_activity_threshold:
        :return:
        """

        # TODO: Move the diff methods here
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

    def classify_accelero(self, diff_class, time_geo, data_accelero):
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
                print("len(diff_list)=", len(diff_list))
                temp_list = []
                temp_diff_list = []

        # Remaining values
        a = len(self.data_geo) - len(diff_list)
        if a > 0:
            for i in range(a):
                diff_list.append(1)
        elif a < 0:
            diff_list.pop()

        self.data_geo["DIFF CLASS"] = diff_list

        # TODO: move this
        self.data_geo.to_csv("data/processed/test.csv")

    def public_transport(self):
        """

        :return:
        """
        activity = []

        for i in range(len(self.data_geo)):
            if Classification.read_api_train(self.data_geo["LAT"][i], self.data_geo["LON"][i])[1]:
                activity.append("Train")
            elif self.data_geo["SPEED"][i] >= 10:
                activity.append("Driving")
            elif self.data_geo["SPEED"][i] < 1.5:
                activity.append("Stationary")
            else:
                activity.append("Walking")

            # TODO: remove the elifs and else:
            # TODO: make a method where all paramters is combined.

        self.data_geo["TRANSPORT"] = activity

    def stops(self):
        """

        :return:
        """
        stops = []

        for i in range(len(self.data_geo)):
            temp = (Classification.read_api_bus(self.data_geo["LAT"][i], self.data_geo["LON"][i]))
            stops.append(temp[2])
        self.data_geo["STOPS"] = stops

    @staticmethod
    def bus(data_geo):
        pass


    def smooth_data(self):
        """
        Inactive
        :return:
        """
        # TODO: try this on raw accelerometer data as well
        for counter in range(len(self.data_geo)):
            temp_diff_class = self.data_geo["DIFF CLASS"][counter]
            print(temp_diff_class)

        # TODO: Not sure how to this smart, maybe try to get the classification in diff classes better to start with

    def line_index(self):
        """
        Inactive
        :return:
        """
        # TODO: make new indexes for lines
        line_index = []
        id = 0
        for i in range(len(self.data_geo)-1):
            if (self.data_geo["DIFF CLASS"][i]) == (self.data_geo["DIFF CLASS"][i+1]):
                line_index.append(id)
            else:
                line_index.append(id)
                id += 1
        line_index.append(id)
        print(len(line_index))
        print(len(self.data_geo))
        print(line_index)

        self.data_geo["LINE ID"] = line_index

        # TODO: Get this to work properly, must have at least two cordinate pairs
        # TODO: dont really need lines

    def fuzzy(self):
        transport = 20
        # stationary = 2


        stationary = 1
        walking = 2
        running = 3
        cycling = 4
        car = 5
        public_transport = 6


        b = []
        classification = []

        for counter in range(len(self.data_geo)):
            temp_class = []
            temp_stationary = 0         # 1
            temp_walking = 0            # 2
            temp_running = 0            # 3
            temp_cycling = 0            # 4
            temp_car = 0                # 5
            temp_public_transport = 0   # 6
            a = ""

            dict_class = {}
            for i in range(1,7):
                dict_class[i] = 0

            if self.data_geo["SPEED"][counter] >= transport:
                # Possibly transport or cycling
                # else: Possibly cycling and running, most likely walking or stationary
                print(counter, "Speed ", self.data_geo["SPEED"][counter], self.data_geo["ACTIVITY"][counter])
                a = a + "Possibly Transport or cycling "
                temp_class.append([car, 0.8])
                temp_car += 0.8
                dict_class[car] += 0.8

                temp_class.append([public_transport, 0.8])
                temp_public_transport += 0.8
                dict_class[public_transport] += 0.8

                temp_class.append([cycling, 0.3])
                temp_cycling += 0.3
                dict_class[cycling] += 0.3

                temp_class.append([running, 0.1])
                temp_running += 0.1
                dict_class[running] += 0.1

            if not self.data_geo["SPEED"][counter] >= transport:
                a = a + "Most likely walking or stationary, Possibly cycling or running "
                temp_class.append([stationary, 0.8])
                temp_stationary += 0.8
                dict_class[stationary] += 0.8

                temp_class.append([walking, 0.8])
                temp_walking += 0.8
                dict_class[walking] += 0.8

                temp_class.append([running, 0.5])
                temp_running += 0.5
                dict_class[running] += 0.5

                temp_class.append([cycling, 0.4])
                temp_cycling += 0.4
                dict_class[cycling] += 0.4

                temp_class.append([public_transport, 0.2])
                temp_public_transport += 0.2
                dict_class[public_transport] += 0.2

                temp_class.append([car, 0.1])
                temp_car += 0.1
                dict_class[car] += 0.1

            if self.data_geo["DIFF CLASS"][counter] > 10:
                # TODO: use all diff classes
                # Possibly cycling, walking or runnning. A sort of activity
                # else:  Transport or stationary
                print(counter, "DIFF CLASS ", self.data_geo["DIFF CLASS"][counter], self.data_geo["ACTIVITY"][counter])
                a = a + "A sort of activity, possibly cycling or walking or running "
                temp_class.append([walking, 0.7])
                temp_walking += 0.7
                dict_class[walking] += 0.7

                temp_class.append([running, 0.5])
                temp_running += 0.5
                dict_class[running] += 0.5

                temp_class.append([cycling, 0.4])
                temp_cycling += 0.4
                dict_class[cycling] += 0.4

            if not self.data_geo["DIFF CLASS"][counter] > 10:
                a = a + "Transport or stationary "
                temp_class.append([stationary, 0.8])
                temp_stationary += 0.8
                dict_class[stationary] += 0.8

                temp_class.append([car, 0.7])
                temp_car += 0.7
                dict_class[car] += 0.7

                temp_class.append([public_transport, 0.7])
                temp_public_transport += 0.7
                dict_class[public_transport] += 0.7

            if self.data_geo["ACCURACY"][counter] > 15:
                # Indoor, Possibly Public transport or driving
                print(counter, "ACCURACY ", self.data_geo["ACCURACY"][counter], self.data_geo["ACTIVITY"][counter])
                a = a + "Indoor, possibly transport "
                temp_class.append([stationary, 0.8])
                temp_stationary += 0.8
                dict_class[stationary] += 0.8

                temp_class.append([public_transport, 0.3])
                temp_public_transport += 0.3
                dict_class[public_transport] += 0.3

                temp_class.append([car, 0.2])
                temp_car += 0.2
                dict_class[car] += 0.4

            if not self.data_geo["ACCURACY"][counter] > 15:
                a = a + "Pretty good accuracy "

            if self.data_geo["ANGLE"][counter] < 5:
                print(counter, "ANGLE ", self.data_geo["ANGLE"][counter], self.data_geo["ACTIVITY"][counter])
                a = a + "Angle is less than 5 "
            if not self.data_geo["ANGLE"][counter] < 5:
                a = a + "Angle is more than 5 "

            if self.data_geo["TIME DIFF"][counter] > 4:
                # Probably Stationary
                # Correlates with Speed
                print(counter, "TIME DIFF ", self.data_geo["TIME DIFF"][counter], self.data_geo["ACTIVITY"][counter])
                a = a + "Probably stationary "
            if not self.data_geo["TIME DIFF"][counter] > 4:
                a = a + "Probably moving "


            if self.data_geo["TRANSPORT"][counter] == "Train":
                temp_class.append([public_transport, 0.9])
                temp_public_transport += 0.9
                dict_class[public_transport] += 0.
            if not self.data_geo["TRANSPORT"][counter] == "Train":
                pass
        # TODO: Loop through the if sentences, find possibilites, then decide most probable

            classification.append(max(dict_class.items(), key=operator.itemgetter(1))[0])

        self.data_geo["CLASSIFICATION"] = classification

if __name__ == "__main__":
    pass
