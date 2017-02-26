# -*- coding: utf-8 -*-

from prepareData import PrepareData
from classification import Classification
from geoViz import GeoViz
from plot import Plot

__author__ = 'eirikaa'


class Simulation:
    def __init__(self):
        pass

    @staticmethod
    def classification():

        ### CLASSIFICATION
        prep = PrepareData(geo_file='data/log/02_12_2_geo.csv', accelero_file='data/log/02_12_2_accelero.csv')
        classification = Classification(diff_range=10)
        x, y, z, xyz, time_accelero, readable_time_accelero, activity, activity2, data_accelero = prep.read_accelerometer_data()
        lat, lon, speed, accuracy, altitude, heading, time_geo, readable_time_geo, activity, activity2, data_geo = prep.read_geodata()

        diff_xyz = classification.diff_maxmin(xyz)
        diff_class = classification.differentiate(diff_xyz, xyz, time_accelero)
        Classification.classify_geo_data(diff_class, time_geo, data_accelero, data_geo)
        # Classification.write_csv(data_geo, diff_class)

        Classification.smooth_data(data_geo)

        GeoViz.make_geojson(data_geo, filename="data/processed/test2.geojson")
        ###

    @staticmethod
    def plot():

        ### PLOT
        prep = PrepareData(geo_file='data/log/02_18_geo.csv', accelero_file='data/log/02_18_accelero.csv')
        classification = Classification(diff_range=10)
        x, y, z, xyz, time, readable_time_acclero, activity, activity2, data = prep.read_accelerometer_data()
        lat, lon, speed, accuracy, altitude, heading, time_geo, readable_time_geo, activity, activity2, data_geo = prep.read_geodata()

        # diff_xyz = ana.diff_maxmin(x, y, z, xyz)
        diff_xyz = classification.diff_avg(xyz)
        print ('diff_xyz', len(diff_xyz))
        classification.diff_sum_variance(xyz)
        diff_class = classification.differentiate(diff_xyz, xyz, time)

        print(prep.calibration(xyz))

        # Plot.plot(x, y, z, xyz, time, diff_class)
        clean_diff_class = []
        for i in diff_class:
            clean_diff_class.append(i[0])
        print(clean_diff_class)
        Plot.plot(x, y, z, xyz, readable_time_acclero, clean_diff_class, speed, time_geo)


        # classification.classify_geo_data(diff_class,time_geo,data,data_geo)
        # Plot.plot(x, y, z, xyz, time, data_geo['Diff class'], speed, time_geo)

        ###

if __name__ == "__main__":

    # Simulation.classification()
    Simulation.plot()