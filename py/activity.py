# -*- coding: utf-8 -*-

from prepareData import PrepareData
import pandas as pd
import matplotlib.pyplot as plt

__author__ = 'eirikaa'

class Plot:
    def __init__(self):
        pass

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

if __name__ == "__main__":
    ana = PrepareData(filename='data/exampledata/spinning_accelero.csv')
    x, y, z, xyz, time, activity, activity2 = ana.read_accelerometer_data()
    diff_xyz = ana.diff(x, y, z, xyz)
    print(diff_xyz)
    diff_class = ana.classify(diff_xyz)
    print(len(diff_class))
    print(len(xyz))
    diff_class.append(1)
    diff_class.append(1)
    diff_class.append(1)
    diff_class.append(1)
    diff_class.append(1)
    # diff_class.append(1)
    # diff_class.append(1)
    # diff_class.append(1)
    # diff_class.append(1)
    # diff_class.append(1)
    #TODO: Make diff_class a seperate method

    Plot.plot(x, y, z, xyz, time, diff_class)