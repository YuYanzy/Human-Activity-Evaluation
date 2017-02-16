# -*- coding: utf-8 -*-

from prepareData import PrepareData
__author__ = 'eirikaa'


class Simulation:
    def __init__(self):
        pass

    @staticmethod
    def sim():
        ana = PrepareData(geo_file='data/log/02_05_geo.csv', accelero_file='data/log/02_05_accelero.csv',
                          diff_range=10)
        x, y, z, xyz, time_accelero, activity, activity2, data_accelero = ana.read_accelerometer_data()
        lat, lon, speed, accuracy, altitude, heading, time_geo, activity, activity2, data_geo = ana.read_geodata()
        diff_xyz = ana.diff_avg(x, y, z, xyz)
        diff_class = ana.classify(diff_xyz, xyz, time_accelero)
        print(len(diff_class))
        print(diff_class)

        # for i in range (len(data_geo)):
        #     print (min(diff_class[i][1], key=lambda x:abs(x-data_geo['TIME'])))
        #     print (diff_class[i][0])
        b = []
        for i in range(len(data_geo)):

            a = (min(data_geo['TIME'], key=lambda x: abs(x - diff_class[i][1])))
            # b.append([a, diff_class[i][0], diff_class[i][1]])
            b.append(diff_class[i][0])
            # b.append()


            # print(diff_class[i][1])
            # print(j)
        # print (data_geo['TIME'])
        # print(b[1][1])
        # print(len(b[:][1]))
        # print(len(data_geo))
        data_geo['Diff class'] = b
        print (data_geo)
        data_geo.to_csv("data/processed/test.csv")
        # print (b[0][1])
        # for i,j  in enumerate (b):
        #     print (j[i][1])
        # print (data_geo)
if __name__ == "__main__":

    Simulation.sim()