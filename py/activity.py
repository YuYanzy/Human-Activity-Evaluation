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

    @staticmethod
    def leaflet(data):
        import folium
        import json
        # map_osm = folium.Map(location=[59.66550801,10.77625199])
        # map_osm.save("osm.html")
        buoy_map = folium.Map(
            [59.66550801,10.77625199],
            zoom_start=7,
            tiles='Stamen Terrain'
        )

        folium.RegularPolygonMarker(
            [59.66550801,10.77625199],
            fill_color='#43d9de',
            radius=12,
            popup=folium.Popup(max_width=450).add_child(
                folium.Vega(json.load(open(data)), width=450, height=250))
        ).add_to(buoy_map)

        buoy_map.save('NOAA_buoys.html')

if __name__ == "__main__":
    ana = PrepareData(geo_file='', accelero_file='data/exampledata/tredemolle_accelero.csv')
    x, y, z, xyz, time, activity, activity2, data = ana.read_accelerometer_data()
    diff_xyz = ana.diff(x, y, z, xyz)
    diff_class = ana.classify(diff_xyz)

    print(ana.calibration(xyz))
    diff_class.append(1)
    diff_class.append(1)
    # diff_class.append(1)
    # diff_class.append(1)
    # diff_class.append(1)
    # diff_class.append(1)
    # diff_class.append(1)
    # diff_class.append(1)
    # diff_class.append(1)
    # # diff_class.append(1)
    print(len(diff_class))
    print(len(xyz))
    print(max(xyz))
    # #TODO: Make diff_class a seperate method
    Plot.plot(x, y, z, xyz, time, diff_class)
    #
