# -*- coding: utf-8 -*-

from PrepareData import AnalyseAccelerometer
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
    pass