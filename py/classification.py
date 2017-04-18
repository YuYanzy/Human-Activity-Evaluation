# -*- coding: utf-8 -*-

import requests
import json
import math
import operator
import sys
sys.path.append('D:/Skole/master/github/dataCapture/py/PostGIS_queries')
import station
import tog
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

    @staticmethod
    def read_api_train(lat, lon):
        """

        :param lat:
        :param lon:
        :return:
        """

        # req = requests.get('http://188.166.168.99/tog/?lon=' + str(lon) + '&lat=' + str(lat))
        # req = req.content.decode(req.apparent_encoding)
        # req = json.loads(req)
        # return req
        req = tog.buss(lon, lat)
        return req

    @staticmethod
    def read_api_bus(lat, lon):
        """

        :param lat:
        :param lon:
        :return:
        """
        # req = requests.get('http://188.166.168.99/buss/?lon=' + str(lon) + '&lat=' + str(lat))
        # req = req.content.decode(req.apparent_encoding)
        # req = json.loads(req)
        # return req

        req = station.sql(lon, lat)
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

    def public_transport(self):
        """

        :return:
        """
        activity = []

        for i in range(len(self.data_geo)):
            if Classification.read_api_train(self.data_geo["LAT"][i], self.data_geo["LON"][i])[1]:
                activity.append("Train")
                print(i, activity)
            else:
                activity.append("Not train")
                print(i, activity)
        self.data_geo["TRANSPORT"] = activity

    def stops(self):
        """

        :return:
        """
        stops = []

        for i in range(len(self.data_geo)):
            temp = (Classification.read_api_bus(self.data_geo["LAT"][i], self.data_geo["LON"][i]))
            stops.append(temp[2])
            print(i, temp)
        self.data_geo["STOPS"] = stops

    def bus(self, transport):
        """
        A segment will contains values of 5 or 1 which mean car or moving. If one of the first 4 elements and the
        last 4 element from the segments correlates with busstop the segment wil be classified as 
        bus/public trasport
         
        :param: transport, classification which contains transport, activity and stationary
        :return: classification, classification list which classifies transport into bus trips
        """
        # TODO: maybe just stationary between car
        # TODO: 02_18 example, the first two elements is a segment and for loops for checking stops dont work
        # tODO need some kind of smoothing, misclassified points breaks this
        segment = []
        temp_start = []
        temp_stop = []
        classification = []
        for counter in range(len(self.data_geo)):
            print(counter)
            # if counter == len(self.data_geo)-1:
            #
            #     for i in range(len(segment)):
            #         classification.append(i)
            # TODO: if sements end on 1 or 5, i have problem now
            if transport[counter] == 5 or transport[counter] == 1 or transport[counter] == 6:
                segment.append(self.data_geo["ID"][counter])
            elif len(segment) > 1:
                # if len(segment) > 1:
                print(segment)
                print(min(segment))
                print(max(segment))
                print(int(max(segment)) - int(min(segment)))
                print(type(int(min(segment))))
                # TODO: this dont match with small segments

                for start in range(int(min(segment)), int(min(segment))+4):
                    if self.data_geo["STOPS"][start]:
                        temp_start.append(1)
                if (int(max(segment)) - 3) >= 0:
                    for stop in range(int(max(segment)) - 3, int(max(segment)) + 1):
                        if self.data_geo["STOPS"][stop]:
                            temp_stop.append(1)
                else:
                    temp_stop.append(0)

                if 1 in temp_start and 1 in temp_stop:
                    print("true")
                    for seg in range(len(segment)):
                        classification.append(6)

                else:
                    for seg in range(int(min(segment)), int(max(segment))+1):
                        classification.append(transport[seg])

                classification.append(transport[counter])
                segment = []
                temp_stop = []
                temp_start = []

            else:
                if len(segment) == 1:
                    classification.append(transport[counter-1])

                classification.append(transport[counter])
                segment = []

            # TODO this is bad
            # TODO: make a rule to check if the segment is at least 5 elements?

            if counter == len(self.data_geo)-1:
                if len(segment) == 0:
                    break
                elif len(segment) > 6:
                    print("Finish the bus method")
                    for start in range(int(min(segment)), int(min(segment))+4):
                        if self.data_geo["STOPS"][start]:
                            temp_start.append(1)

                    for stop in range(int(max(segment)) - 3, int(max(segment)) + 1):
                        if self.data_geo["STOPS"][stop]:
                            temp_stop.append(1)

                    if 1 in temp_start and 1 in temp_stop:
                        print("true")
                        for seg in range(len(segment)):
                            classification.append(6)

                    else:
                        for i in range(int(min(segment)), int(max(segment)) + 1):
                            classification.append(transport[i])

                else:
                    for i in range(int(min(segment)), int(max(segment))+1):
                        classification.append(transport[i])

            print(classification)
            print(len(classification))
        # TODO: if speed correlates with busstops
        return classification

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
        line_id = 0
        for i in range(len(self.data_geo)-1):
            if (self.data_geo["DIFF CLASS"][i]) == (self.data_geo["DIFF CLASS"][i+1]):
                line_index.append(line_id)
            else:
                line_index.append(line_id)
                line_id += 1
        line_index.append(line_id)
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

        classification = []

        for counter in range(len(self.data_geo)):
            a = ""

            dict_class = {}
            for i in range(1, 7):
                dict_class[i] = 0

            if self.data_geo["SPEED"][counter] >= transport:
                # Possibly transport or cycling
                # else: Possibly cycling and running, most likely walking or stationary
                print(counter, "Speed ", self.data_geo["SPEED"][counter], self.data_geo["ACTIVITY"][counter])
                a = a + "Possibly Transport or cycling "
                dict_class[car] += 0.8
                dict_class[public_transport] += 0.8
                dict_class[cycling] += 0.3
                dict_class[running] += 0.1

            if self.data_geo["SPEED"][counter] < transport and self.data_geo["SPEED"][counter] > 3:
                dict_class[stationary] += 0.1
                dict_class[walking] += 0.9
                dict_class[running] += 0.6
                dict_class[cycling] += 0.5
                dict_class[public_transport] += 0.3
                dict_class[car] += 0.2

            if self.data_geo["SPEED"][counter] < 3:
                a = a + "Most likely walking or stationary, Possibly cycling or running "
                dict_class[stationary] += 0.8
                dict_class[walking] += 0.3
                dict_class[running] += 0.2
                dict_class[cycling] += 0.1
                dict_class[public_transport] += 0.1
                dict_class[car] += 0.1

            if self.data_geo["DIFF CLASS"][counter] == 25:
                # TODO: use all diff classes
                # Possibly cycling, walking or runnning. A sort of activity
                # else:  Transport or stationary
                print(counter, "DIFF CLASS ", self.data_geo["DIFF CLASS"][counter], self.data_geo["ACTIVITY"][counter])
                a = a + "A sort of activity, possibly cycling or walking or running "
                dict_class[walking] += 0.7
                dict_class[running] += 0.5
                dict_class[cycling] += 0.4

            if self.data_geo["DIFF CLASS"][counter] == 30:
                dict_class[running] += 1
                dict_class[walking] += 0.5
                dict_class[cycling] += 0.7

            if self.data_geo["DIFF CLASS"][counter] == -15:
                a = a + "Transport or stationary "
                dict_class[stationary] += 0.8
                dict_class[car] += 0.7
                dict_class[public_transport] += 0.7

            if self.data_geo["ACCURACY"][counter] > 15:
                # Indoor, Possibly Public transport or driving
                print(counter, "ACCURACY ", self.data_geo["ACCURACY"][counter], self.data_geo["ACTIVITY"][counter])
                a = a + "Indoor, possibly transport "
                dict_class[stationary] += 0.8
                dict_class[public_transport] += 0.3
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
                dict_class[public_transport] += 0.9

            if not self.data_geo["TRANSPORT"][counter] == "Train":
                pass

            print(dict_class)
            classification.append(max(dict_class.items(), key=operator.itemgetter(1))[0])

        self.data_geo["CLASSIFICATION"] = classification

    def fuzzy2(self):

        stationary = 1
        walking = 2
        running = 3
        cycling = 4
        car = 5
        public_transport = 6

        classification1 = []
        classification2 = []
        classification3 = []
        classification4 = []

        for counter in range(len(self.data_geo)):
            dict_class = {}
            for i in range(1, 4):
                dict_class[i] = 0

            # 1 = Stationary
            # 2 = Moving
            # 3 = Unknown

            if self.data_geo["SPEED"][counter] > 5:
                dict_class[2] += 10
                dict_class[stationary] += 0

            elif self.data_geo["SPEED"][counter] <= 5 and self.data_geo["SPEED"][counter] > 2:
                dict_class[2] += 7
                dict_class[stationary] += 3

            elif self.data_geo["DIFF CLASS"][counter] > 10:
                dict_class[2] += 5

            else:
                dict_class[stationary] += 10
            classification1.append(max(dict_class.items(), key=operator.itemgetter(1))[0])

        # MOVEMENT
        for counter in range(len(self.data_geo)):
            dict_class = {}
            for i in range(2, 4):
                dict_class[i] = 0

                # 2 = Transport
                # 3 = Activity

            if classification1[counter] == 2:

                if self.data_geo["DIFF CLASS"][counter] == 30:
                    dict_class[3] += 10
                if self.data_geo["DIFF CLASS"][counter] == 25:
                    dict_class[3] += 5
                    dict_class[2] += 2
                if self.data_geo["DIFF CLASS"][counter] == -15:
                    dict_class[3] += 2
                    dict_class[2] += 7
                if self.data_geo["SPEED"][counter] > 40:
                    dict_class[2] += 6
                if self.data_geo["SPEED"][counter] <= 40 and self.data_geo["SPEED"][counter] > 20:
                    dict_class[2] += 4
                classification2.append(max(dict_class.items(), key=operator.itemgetter(1))[0])
            else:

                classification2.append(classification1[counter])

        # TRANSPORT
        for counter in range(len(self.data_geo)):
            dict_class = {}
            for i in range(5, 7):
                dict_class[i] = 0

                # 5 = Car
                # 6 = Public transport
            if classification2[counter] == 2:

                if self.data_geo["TRANSPORT"][counter] == "Train":
                    dict_class[public_transport] += 10
                if not self.data_geo["TRANSPORT"][counter] == "Train":
                    dict_class[car] += 10

                classification3.append(max(dict_class.items(), key=operator.itemgetter(1))[0])
            else:
                classification3.append(classification2[counter])

        bus = self.bus(classification3)
        print("len(classification3")
        print(len(classification3))
        print("classification3")
        print(classification3)

        print("len(bus")
        print(len(bus))
        print("bus")
        print(bus)
        classification3 = bus
        # TODO: why?
        # try:
        #     self.data_geo["CLASSIFICATION"] = classification3
        # except ValueError:
        #     classification3.append(10)
        #     self.data_geo["CLASSIFICATION"] = classification3

        # ACTIVITY
        for counter in range(len(self.data_geo)):
            dict_class = {}
            for i in range(2, 5):
                dict_class[i] = 0

                # 2 = Walking
                # 3 = Running
                # 4 = Cycling

            if classification2[counter] == 3:
                if self.data_geo["SPEED"][counter] < 8:
                    dict_class[walking] += 10
                    dict_class[running] += 4
                    dict_class[cycling] += 2
                if self.data_geo["SPEED"][counter] >= 8 and self.data_geo["SPEED"][counter] < 16:
                    dict_class[walking] += 1
                    dict_class[running] += 9
                    dict_class[cycling] += 6
                # TODO: make smaller gaps to adjust the possibility
                if self.data_geo["SPEED"][counter] >= 16:
                    dict_class[running] += 2
                    dict_class[cycling] += 10

                if self.data_geo["DIFF CLASS"][counter] == 25:
                    dict_class[walking] += 8
                    dict_class[running] += 2
                    dict_class[cycling] += 5
                if self.data_geo["DIFF CLASS"][counter] == 30:
                    dict_class[walking] += 2
                    dict_class[running] += 6
                    dict_class[cycling] += 5
                if self.data_geo["DIFF CLASS"][counter] == -15:
                    dict_class[cycling] += 8
                classification4.append(max(dict_class.items(), key=operator.itemgetter(1))[0])
            else:
                classification4.append(classification3[counter])

        self.data_geo["CLASSIFICATION"] = classification4

        # TODO: is it necessary to split activiies? Will give worse results
        # TODO: split this into more methods, recursive?

    def correlation(self):

        correlation = []
        for counter in range(len(self.data_geo)):
            if self.data_geo["TRUE ACTIVITY NUM"][counter] == self.data_geo["CLASSIFICATION"][counter]:
                correlation.append("True")
            else:
                correlation.append("False")

        self.data_geo["CORRELATION"] = correlation

    def num2text(self):
        stationary = 1
        walking = 2
        running = 3
        cycling = 4
        car = 5
        public_transport = 6
        unknown = 10

        activity = []
        for counter in range(len(self.data_geo)):
            if self.data_geo["CLASSIFICATION"][counter] == stationary:
                activity.append("Stationary")
            elif self.data_geo["CLASSIFICATION"][counter] == walking:
                activity.append("Walking")
            elif self.data_geo["CLASSIFICATION"][counter] == running:
                activity.append("Running")
            elif self.data_geo["CLASSIFICATION"][counter] == cycling:
                activity.append("Cycling")
            elif self.data_geo["CLASSIFICATION"][counter] == car:
                activity.append("Car")
            elif self.data_geo["CLASSIFICATION"][counter] == public_transport:
                activity.append("Public transport")
            else:
                activity.append("Unknown")

        self.data_geo["CLASSIFICATION TEXT"] = activity

if __name__ == "__main__":
    pass
