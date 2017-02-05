# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import csv

__author__ = 'eirikaa'


class AnalyseAccelerometer:
    """

    """
    def __init__(self, filename):
        """

        :param filename:
        """
        self.filename = filename

    def readcsv(self):
        """

        :return:
        """
        x = []
        y = []
        z = []
        xyz = []
        time = []
        activity = []

        csvfile = open(self.filename, "r")
        csv_reader = csv.reader(csvfile, delimiter=" ")
        for row in csv_reader:
            if not(float(row[1]) == 0.0 and float(row[2]) == 0.0 and float(row[3]) == 0.0):
                x.append(float(row[1]))
                y.append(float(row[2]))
                z.append(float(row[3]))
                xyz.append(float(row[4]))
                time.append(float(row[5]))
                activity.append(row[6])

        return x, y, z, xyz, time, activity

    @staticmethod
    def plot(x, y, z, xyz, time, diff_class):
        """

        :param x:
        :param y:
        :param z:
        :param xyz:
        :param time:
        :param diff_class:
        :return:
        """

        # Plot XYZ data
        plt.plot(time, xyz, "r", label="xyz")
        plt.plot(time, diff_class, "bo", label="movement")
        plt.axis([min(time), max(time), min(diff_class)-5, max(diff_class)+5])
        plt.show()

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
        hard_activity_threshold = 20

        activity = 40
        hard_activity = 45
        low_activity = -40
        # FIXME: fix this
        diff_class = []

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
                diff_class.append(40)
                diff_class.append(40)
                diff_class.append(40)
                diff_class.append(40)
                diff_class.append(40)
                diff_class.append(40)
                diff_class.append(40)
                diff_class.append(40)
                diff_class.append(40)
                diff_class.append(40)

            else:
                diff_class.append(-40)
                diff_class.append(-40)
                diff_class.append(-40)
                diff_class.append(-40)
                diff_class.append(-40)
                diff_class.append(-40)
                diff_class.append(-40)
                diff_class.append(-40)
                diff_class.append(-40)
                diff_class.append(-40)

        return diff_class

if __name__ == '__main__':
    ana = AnalyseAccelerometer(filename='data/log/02_05_accelero.csv')
    x, y, z, xyz, time, activity = ana.readcsv()
    diff_xyz = ana.diff(x, y, z, xyz)
    diff_class = ana.classify(diff_xyz)

    diff_class.append(1)
    diff_class.append(1)
    diff_class.append(1)
    diff_class.append(1)
    diff_class.append(1)
    diff_class.append(1)
    diff_class.append(1)

    print(len(diff_class))
    print(len(xyz))
    ana.plot(x, y, z, xyz, time, diff_class)
