# -*- coding: utf-8 -*-

from prepareData import PrepareData
import pandas as pd
import matplotlib.pyplot as plt

__author__ = 'eirikaa'

class Plot:
    def __init__(self):
        pass

    @staticmethod
    def plot(x, y, z, xyz, time, diff_class, speed, geo_time):
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
        # plt.ion()
        plt.plot(time, xyz, "r", label="xyz")
        plt.plot(time, diff_class, "bo", label="movement")
        plt.axis([min(time), max(time), min(diff_class)-5, max(diff_class)+5])
        plt.show()


        # TODO: få med speed i plottet
    @staticmethod
    def plot2(x, y, z, xyz, time, diff_class, speed, geo_time):
        fig, ax1 = plt.subplots()
        ax1.plot(time, xyz)

        ax2 = ax1.twinx()
        ax2.plot(geo_time, speed, "r")
        # plt.plot(geo_time, speed, "r", label="speed")
        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    ana = PrepareData(geo_file='data/log/02_14_geo.csv', accelero_file='data/log/02_14_accelero.csv', diff_range=15)
    x, y, z, xyz, time, activity, activity2, data = ana.read_accelerometer_data()
    lat, lon, speed, accuracy, altitude, heading, time_geo, activity, activity2, data_geo = ana.read_geodata()

    # diff_xyz = ana.diff_maxmin(x, y, z, xyz)
    diff_xyz = ana.diff_avg(x, y, z, xyz)
    diff_class = ana.classify(diff_xyz, xyz, time)

    print (diff_class)
    print(ana.calibration(xyz))
    print (len(diff_class))
    print (len(xyz))


    # #TODO: Make diff_class a seperate method
    # Plot.plot(x, y, z, xyz, time, diff_class)
    a = []
    for i in diff_class:
       a.append(i[0])
    print (a)
    Plot.plot2(x, y, z, xyz, time, a, speed, time_geo)