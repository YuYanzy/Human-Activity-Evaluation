from prepareData import PrepareData
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

def geo_viz(points):
    # TODO: Folium, geopandas

    points['geometry'] = points.apply(lambda z: Point(z.LON, z.LAT), axis=1)
    data_frame = gpd.GeoDataFrame(points)
    print (points)
    data_frame.plot()
    plt.show()


if __name__ == "__main__":

    ana = PrepareData("data/log/02_03_geo.csv")
    lat, lon, accuracy, altitude, heading, time, activity, activity2, data = ana.read_geodata()
    geo_viz(data)