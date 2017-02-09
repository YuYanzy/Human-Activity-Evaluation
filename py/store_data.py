# -*- coding: utf-8 -*-

import os
from flask import Flask, request  #, jsonify
from flask_jsonpify import jsonify
import csv
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
        # csv_writer = csv.writer(open(output_csv, "w"))

        # # csv_writer.writerow(["Index", "Lat", "Lon", "Speed", "Accuracy", "AltitudeAccuracy", "Heading", "X", "Y", "Z", "Time"])
        # csv_writer.writerow(["bla", lat, lon, speed, accuracy, altitudeAcurracy, heading, x, y, z, '\r\n'])
        # TODO: this must be moved, not sure how to solve this
        # TODO: Maybe move a file to a storage after it has produced so many lines

        i = 0
        # if os.path.exists(output_name + str(i) + fileformat):
        #     if bufcount(output_name + str(i) + fileformat) > 10:
        #         i += 1

        with open('data/'+output_GNSS + str(i) + fileformat, "a+") as f:
            f.write("bla" + ", " + str(lat) + ", " + str(lon) + ", " + str(speed) + ", " + str(accuracy) + ", " +
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

    # TODO: fikse time? og heller konvertere ved plott?

    write_csv(lat, lon, speed, accuracy, altitude, heading, time.time(), activity)
    return jsonify("bla" + ", " + str(lat) + ", " + str(lon) + ", " + str(speed) + ", " + str(accuracy) + ", " + str(altitude) + ", "
                    + str(heading) + ", " + str(time.time()) + ", " + str(activity))


@app.route("/storeACCELEROMETER")
def store_accelerometer(x=X,y=Y,z=Z, activity = ACTIVITY):
    def write_csv(x, y, z, time, activity, output_accelerometer=ACCELEROMETER_OUTPUT, fileformat=FILEFORMAT):
        # csv_writer = csv.writer(open(output_csv, "w"))
        # # csv_writer.writerow(["Index", "Lat", "Lon", "Speed", "Accuracy", "AltitudeAccuracy", "Heading", "X", "Y", "Z", "Time"])
        # csv_writer.writerow(["bla", lat, lon, speed, accuracy, altitudeAcurracy, heading, x, y, z, '\r\n'])
        # TODO: this must be moved, not sure how to solve this
        # TODO: Maybe move a file to a storage after it has produced so many lines

        i = 0
        # if os.path.exists(output_name + str(i) + fileformat):
        #     if bufcount(output_name + str(i) + fileformat) > 10:
        #         i += 1

        with open('data/'+output_accelerometer + str(i) + fileformat, "a+") as f:
            f.write(
                "bla" + ", " + str(x) + ", " + str(y) + ", " + str(z) + ", "+ str((math.sqrt((x)**2+(y)**2+(z)**2))-9.81) + ", " + str(time) + ", " + str(activity) + " " + "\n")

    # ACCELEROMETER
    x = float((request.args.get("x", x)))
    y = float((request.args.get("y", y)))
    z = float((request.args.get("z", z)))

    # TRUTH DATA
    activity = (request.args.get("activity", activity))

    # TODO: fikse time? og heller konvertere ved plott?
    write_csv(x, y, z, time.time(), activity)

    return jsonify("bla" + ", " + str(x) + ", " + str(y) + ", " + str(z) + ", " + str((math.sqrt((x)**2+(y)**2+(z)**2))-9.81) +", " + str(time.time()) + ", " + str(activity))



def bufcount(filename):
    f = open(filename)
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read  # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    return lines


if __name__ == '__main__':
     app.run(host='0.0.0.0', debug=True)