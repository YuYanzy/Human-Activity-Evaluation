from prepareData import PrepareData
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import folium
import json
import vincent

def geo_viz(points):
    # TODO: Folium, geopandas

    points['geometry'] = points.apply(lambda z: Point(z.LON, z.LAT), axis=1)
    data_frame = gpd.GeoDataFrame(points)
    print (points)
    data_frame.plot()
    plt.show()

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

if __name__ == "__main__":

    ana = PrepareData(geo_file="data/log/02_06_geo.csv", accelero_file="data/log/02_06_accelero.csv")
    lat, lon, accuracy, altitude, heading, time, activity, activity2, data_geo = ana.read_geodata()
    # geo_viz(data)

    x, y, z, xyz, time, activity, activity2, data_acc= ana.read_accelerometer_data()
    bar = vincent.Line(data_acc['XYZ'])
    bar.to_json('vega.json')

    leaflet('vega.json')
