from FlaskApp import app
import psycopg2
from flask.ext.jsonpify import jsonify
from flask import request

LON = 10.787869
LAT = 59.662123

@app.route('/scoords/')
def scoordsql(lon=LON, lat=LAT):
    lon = float((request.args.get('lon', lon)))
    lat = float((request.args.get('lat', lat)))

    try:
        conn = psycopg2.connect(dbname='r2o', user='johu',
        password='', host='localhost', port=5432)
    except ValueError:
        print('database ikke tilkoblet')

    sql = ("""with index_query as (
    select ST_Distance(
    geom ::geography,
    ST_POINT({}, {}) ::geography) as distance,
    st_y(geom) as y, st_x(geom) as x, navn as navn
    from n50.stasjoner
        order by geom <-> ST_POINT({}, {}) limit 100
)
select x, y, navn from index_query order by distance limit 5
""").format(lon, lat, lon, lat)

    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return jsonify(rows)
