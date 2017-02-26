from prepareData import PrepareData
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import folium
import json
import vincent

class GeoViz:
    def __init__(self):
        pass

    @staticmethod
    def geopandas_viz(points):
        # TODO: Folium, geopandas

        points['geometry'] = points.apply(lambda z: Point(z.LON, z.LAT), axis=1)
        data_frame = gpd.GeoDataFrame(points)
        print (points)
        data_frame.plot()
        plt.show()

    @staticmethod
    def leaflet(data):
        # map_osm = folium.Map(location=[59.66550801,10.77625199])
        # map_osm.save("osm.html")
        buoy_map = folium.Map(
            [59.66550801,10.77625199],
            zoom_start=14,
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

    @staticmethod
    def leaflet2():
        file = "data/geo/test.geojson"

        map = folium.Map(location=[59.66, 10.77],
                          tiles="Stamen Terrain", zoom_start=7)

        map.add_child(folium.GeoJson(data=open(file),
                                     name="geojson",
                                     ).add_child(
            folium.Popup("simples tring")
        )).add_to(map)
        # folium.GeoJson(data=open(file),
        #                name="geojson",
        #                ).add_child(folium.Popup("Simple popup"))

        map.save("test.html")

    @staticmethod
    def make_geojson(df, filename):
        print (df)
        geometry = [Point(xy) for xy in zip(df.LON, df.LAT)]
        # df = df.drop(["LON", "LAT"], axis=1)
        geo_df = gpd.GeoDataFrame(df, geometry=geometry)
        with open(filename, "w") as f:
            f.write(geo_df.to_json())
        # TODO: make geojson lines


if __name__ == "__main__":

    prep = PrepareData(geo_file="data/log/02_14_geo.csv", accelero_file="data/log/02_12_2_accelero.csv")
    lat, lon, speed, accuracy, altitude, heading, time, readable_time, activity, activity2, data_geo = prep.read_geodata()
    GeoViz.geopandas_viz(data_geo)


    x, y, z, xyz, time, readable_time_acclero, activity, activity2, data_acc= prep.read_accelerometer_data()
    bar = vincent.Line(data_acc['XYZ'])
    bar.to_json('vega.json')

    # leaflet('vega.json')
    # leaflet2()

    # print (data_acc["XYZ"][3:5])
    #
    # for i in range(len(data_acc["XYZ"])-10):
    #     vincent.Line(data_acc['XYZ'][i:i+10]).to_json("data/vega/vega"+str(i)+".json")