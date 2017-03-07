# -*- coding: utf-8 -*-

from prepareData import PrepareData
from classification import Classification
from geoViz import GeoViz
from plot import Plot
import vincent

__author__ = 'eirikaa'


class Simulation:
    def __init__(self, geo_file, accelero_file):

        self.geo_file = geo_file
        self.accelero_file = accelero_file

    def classification(self):

        ### CLASSIFICATION
        prep = PrepareData(geo_file=self.geo_file, accelero_file=self.accelero_file)

        x, y, z, xyz, time_accelero, readable_time_accelero, activity, activity2, data_accelero = prep.read_accelerometer_data()
        lat, lon, speed, accuracy, altitude, heading, time_geo, readable_time_geo, activity, activity2, data_geo = prep.read_geodata()
        classification = Classification(diff_range=10, data_geo=data_geo)

        ### OPTIONAL METHODS
        # diff_xyz = classification.diff_maxmin(xyz)
        # diff_class = classification.differentiate(diff_xyz, xyz, time_accelero, hard_activity_threshold=13, activity_threshold=4)
        # classification.classify_geo_data(diff_class, time_geo, data_accelero)
        # classification.activity()
        classification.stops()
        GeoViz.make_geojson(data_geo, filename="data/processed/test3.geojson")
        ###


    def plot(self):

        ### PLOT
        prep = PrepareData(geo_file=self.geo_file, accelero_file=self.accelero_file)
        classification = Classification(diff_range=10, data_geo=self.geo_file)
        x, y, z, xyz, time, readable_time_acclero, activity, activity2, data = prep.read_accelerometer_data()
        lat, lon, speed, accuracy, altitude, heading, time_geo, readable_time_geo, activity, activity2, data_geo = prep.read_geodata()

        # diff_xyz = ana.diff_maxmin(x, y, z, xyz)
        diff_xyz = classification.diff_avg(xyz)
        diff_class = classification.differentiate(diff_xyz, xyz, time)

        print(prep.calibration(xyz))

        # Plot.plot(x, y, z, xyz, time, diff_class)
        clean_diff_class = []
        for i in diff_class:
            clean_diff_class.append(i[0])
        print(clean_diff_class)

        # Can change xyz with data["magNoG"]
        Plot.plot(x, y, z, xyz, readable_time_acclero, clean_diff_class, speed, time_geo)

        # classification.classify_geo_data(diff_class,time_geo,data)
        # Plot.plot(x, y, z, xyz, time, data_geo['Diff class'], speed, time_geo)

        ###

    def viz(self):

        ### GeoViz
        prep = PrepareData(geo_file=self.geo_file, accelero_file=self.accelero_file)
        lat, lon, speed, accuracy, altitude, heading, time, readable_time, activity, activity2, data_geo = prep.read_geodata()
        GeoViz.geopandas_viz(data_geo)

        x, y, z, xyz, time, readable_time_acclero, activity, activity2, data_acc = prep.read_accelerometer_data()
        bar = vincent.Line(data_acc['XYZ'])
        bar.to_json('vega.json')

        # leaflet('vega.json')
        # leaflet2()

        # print (data_acc["XYZ"][3:5])
        #
        # for i in range(len(data_acc["XYZ"])-10):
        #     vincent.Line(data_acc['XYZ'][i:i+10]).to_json("data/vega/vega"+str(i)+".json")

if __name__ == "__main__":

    geo_file = 'data/log/02_12_2_geo.csv'
    accelero_file = 'data/log/02_12_2_accelero.csv'
    sim = Simulation(geo_file, accelero_file)
    sim.classification()
    # sim.plot()
    # sim.viz()
