# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

__author__ = 'eirikaa'


class Plot:
    def __init__(self):
        pass

    @staticmethod
    def plot_xyz(x, y, z, xyz, time, diff_class, speed, geo_time):
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
        plt.plot(time, diff_class, "bo", label="Activity")
        plt.legend()
        plt.gcf().autofmt_xdate()
        plt.axis([min(time), max(time), min(diff_class)-5, max(diff_class)+5])
        plt.show()

        # TODO: få med speed i plottet

    @staticmethod
    def plot_3_axis(x, y, z, time):
        plt.plot(time, x, 'r', label='x-axis')
        plt.plot(time, y, 'b', label='y-axis')
        plt.plot(time, z, 'g', label='z-axis')

        plt.legend()

        plt.gcf().autofmt_xdate()
        plt.axis([min(time), max(time), min(x) - 5, max(y) + 20])
        plt.show()

    @staticmethod
    def plot2(x, y, z, xyz, time, diff_class, speed, geo_time):
        fig, ax1 = plt.subplots()
        ax1.plot(time, xyz)

        ax2 = ax1.twinx()
        ax2.plot(geo_time, speed, "r")
        # plt.plot(geo_time, speed, "r", label="speed")
        fig.tight_layout()
        plt.show()

    @staticmethod
    def count_steps(data_accelero):
        # TODO: findpeaks
        # https://blog.ytotech.com/2015/11/01/findpeaks-in-python/

        import numpy as np
        import peakutils
        from peakutils.plot import plot as pplot

        # cb = np.array(data_accelero["XYZ"])
        cb = data_accelero["XYZ"].as_matrix()

        indexes = peakutils.indexes(cb, thres=8 / max(cb), min_dist=3)
        print(indexes)
        plt.figure(figsize=(10, 6))
        pplot(data_accelero["Time"].as_matrix(), cb, indexes)

        # interpolatedIndexes = peakutils.interpolate(range(0, len(cb)), cb, ind=indexes)
        # interpolatedIndexes = peakutils.interpolate(data_accelero["Time"].as_matrix(), cb, ind=indexes)
        # pplot(data_accelero["Time"].as_matrix(), cb, interpolatedIndexes)

        plt.show()

    @staticmethod
    def confusion_matrix(data_geo):
        y_actu = data_geo["TRUE ACTIVITY NUM"]
        y_pred = data_geo["CLASSIFICATION"]
        df_confusion = pd.crosstab(y_actu, y_pred, rownames=['Actual'], colnames=['Predicted'])#, margins=True)
        df_conf_norm = df_confusion / df_confusion.sum(axis = 1)
        print (pd.crosstab(y_actu, y_pred, rownames=['Actual'], colnames=['Predicted'], margins=True).to_latex())
        print("---------------------------------------------------")
        print(df_conf_norm.to_latex())



        print("---------------------------------------------------")
        from sklearn.metrics import confusion_matrix
        cm = (confusion_matrix(data_geo["TRUE ACTIVITY NUM"], data_geo["CLASSIFICATION"]))
        print (cm)
        print("---------------------------------------------------")
        cm_norm = cm.astype('float') / cm.sum(axis=1)[:,np.newaxis]
        print(cm_norm)
        print("---------------------------------------------------")

        from pandas_ml import ConfusionMatrix
        cm_panda = ConfusionMatrix(data_geo["TRUE ACTIVITY NUM"], data_geo["CLASSIFICATION"])
        print(cm_panda)
        print("---------------------------------------------------")

        # cm_panda.plot(normalized=True)
        cm_panda.print_stats()

        return df_confusion, df_conf_norm

    @staticmethod
    def plot_confusion_matrix(df_confusion, title='Confusion matrix', cmap=plt.cm.gray_r):
        plt.matshow(df_confusion, cmap=cmap)  # imshow
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(df_confusion.columns))
        plt.xticks(tick_marks, df_confusion.columns, rotation=45)
        plt.yticks(tick_marks, df_confusion.index)
        # plt.tight_layout()
        plt.ylabel(df_confusion.index.name)
        plt.xlabel(df_confusion.columns.name)
        plt.show()

    @staticmethod
    def plot_normm_confusion_matrix(df_confusion_norm, title='Confusion matrix', cmap=plt.cm.gray_r):
        plt.matshow(df_confusion_norm, cmap=cmap)  # imshow
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(df_confusion_norm.columns))
        plt.xticks(tick_marks, df_confusion_norm.columns, rotation=45)
        plt.yticks(tick_marks, df_confusion_norm.index)
        # plt.tight_layout()
        plt.ylabel(df_confusion_norm.index.name)
        plt.xlabel(df_confusion_norm.columns.name)
        plt.show()

if __name__ == "__main__":
    pass
