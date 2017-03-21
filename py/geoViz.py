import geopandas as gpd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import folium
import json

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
        # POINTS

        geometry = [Point(xy) for xy in zip(df.LON, df.LAT)]
        df = df.drop(["LON", "LAT"], axis=1)
        geo_df = gpd.GeoDataFrame(df, geometry=geometry)
        with open(filename, "w") as f:
            f.write(geo_df.to_json())

        # LINES

        # line_geo_df = geo_df.groupby(["LINE ID"])["geometry"].apply(lambda x: LineString(x.tolist()))
        # line_geo_df = gpd.GeoDataFrame(line_geo_df, geometry=geometry)
        # print (line_geo_df)



if __name__ == "__main__":
    pass