# -*- coding: utf-8 -*-

from prepareData import PrepareData
from classification import Classification
__author__ = 'eirikaa'


class Simulation:
    def __init__(self):
        pass

    @staticmethod
    def sim():
        prep = PrepareData(geo_file='data/log/02_12_2_geo.csv', accelero_file='data/log/02_12_2_accelero.csv')
        classification = Classification(diff_range=15)
        x, y, z, xyz, time_accelero, activity, activity2, data_accelero = prep.read_accelerometer_data()
        lat, lon, speed, accuracy, altitude, heading, time_geo, activity, activity2, data_geo = prep.read_geodata()
        diff_xyz = classification.diff_avg(x, y, z, xyz)
        diff_class = classification.classify(diff_xyz, xyz, time_accelero)

        tall = 1000
        b = []
        time_geo = list(time_geo)
        print(min(time_geo, key=lambda x: abs(x - diff_class[tall][1])))
        # print(type(list(time_geo)))
        for i in range(len(data_accelero)):

            # a = (min(data_geo['TIME'], key=lambda x: abs(x - diff_class[i][1])))
            a= min(time_geo, key=lambda x: abs(x-diff_class[i][1]))
            b.append([diff_class[i][0],a])
        counter = 0

        temp_list = []
        new_list = []
        diff_list = []
        for j in range(1,len(b)):
            temp_time = b[j][1]
            temp_diff = b[j][0]
            if temp_time == b[j-1][1]:
                temp_list.append(b[j])
                # TODO: is this one nesecary?
                if temp_time != b[j-2][1]:
                    new_list.append(temp_list[0][1])
                    diff_list.append(temp_list[0][0])
                    # TODO: add the diff class with most similar values
                    for i in diff_list:
                        print (i)
            else:
                temp_list = []


        print (len(new_list))
        print (len(data_geo))


            # if temp_time != b[j+1][1] or temp_diff != b[j+1][0]:
            #     counter += 1
            #     print (b[j])
            #     print (counter)


        diff_list.append(1)
        diff_list.append(1)
        diff_list.append(1)
        diff_list.append(1)
        diff_list.append(1)
        data_geo['Diff class'] = diff_list
        data_geo.to_csv("data/processed/test.csv")

if __name__ == "__main__":

    Simulation.sim()