# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_jsonpify import jsonify
import time
import math

__author__ = 'eirikaa'

app = Flask(__name__)

# Geolocation
LAT = 0
LON = 0
SPEED = 0
ACCURACY = 0
ALTITUDE = 0
ALTITUDEACCURACY = 0
HEADING = 0

# Accelerometer
X = 0
Y = 0
Z = 0

# Activity
ACTIVITY = "Unknown"

# Output
GNSS_OUTPUT = "geolocation"
ACCELEROMETER_OUTPUT = "accelerometer"
FILEFORMAT = ".csv"


@app.route("/")
def index():
    html = """<h1>This API will store geodata from an app</h1>
    <p> Use /storeACCELEROMETER?x=[x]&y=[y]&z=[z]&activity=[activity]</p>
    <p> For geolocation use
    <p> Use /storeGNSS?</p>
    """
    return html


@app.route("/storeGNSS")
def store_GNSS(lat=LAT,lon=LON,speed=SPEED,accuracy=ACCURACY,altitude=ALTITUDE,altitudeAcurracy=ALTITUDEACCURACY,heading=HEADING, activity = ACTIVITY):
    def write_csv(lat, lon, speed, accuracy, altitude, heading, time, activity, output_GNSS=GNSS_OUTPUT, fileformat=FILEFORMAT):
        with open('data/'+output_GNSS + fileformat, "a+") as f:
            f.write("ID" + ", " + str(lat) + ", " + str(lon) + ", " + str(speed) + ", " + str(accuracy) + ", " +
                    str(altitude) + ", " + str(heading) + ", " + str(time) + ", " + str(activity) + " " + "\n")

    # GEOLOCATION
    lat = float((request.args.get("lat", lat)))
    lon = float((request.args.get("lon", lon)))
    speed = float((request.args.get("speed", speed)))
    accuracy = float((request.args.get("accuracy", accuracy)))
    altitude = float((request.args.get("altitude", altitude)))
    # altitudeAcurracy = float((request.args.get("altitudeAccuracy", altitudeAcurracy)))
    heading = float((request.args.get("heading", heading)))

    # TRUTH DATA
    activity = (request.args.get("activity", activity))

    write_csv(lat, lon, speed, accuracy, altitude, heading, time.time(), activity)
    return jsonify("ID" + ", " + str(lat) + ", " + str(lon) + ", " + str(speed) + ", " + str(accuracy) + ", " + str(altitude) + ", "
                    + str(heading) + ", " + str(time.time()) + ", " + str(activity))


@app.route("/storeACCELEROMETER")
def store_accelerometer(x=X, y=Y, z=Z, activity=ACTIVITY):
    def write_csv(x, y, z, time, activity, output_accelerometer=ACCELEROMETER_OUTPUT, fileformat=FILEFORMAT):
        with open('data/'+output_accelerometer + fileformat, "a+") as f:
            f.write("ID" + ", " + str(x) + ", " + str(y) + ", " + str(z) + ", " + str((math.sqrt((x)**2+(y)**2+(z)**2))-9.81) + ", " + str(time) + ", " + str(activity) + " " + "\n")

    # ACCELEROMETER
    x = float((request.args.get("x", x)))
    y = float((request.args.get("y", y)))
    z = float((request.args.get("z", z)))

    # TRUTH DATA
    activity = (request.args.get("activity", activity))

    # TODO: fikse time? og heller konvertere ved plott?
    write_csv(x, y, z, time.time(), activity)

    return jsonify("ID" + ", " + str(x) + ", " + str(y) + ", " + str(z) + ", " + str((math.sqrt((x)**2+(y)**2+(z)**2))-9.81) + ", " + str(time.time()) + ", " + str(activity))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
