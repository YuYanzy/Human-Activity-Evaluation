import psycopg2

LON = 10.787869
LAT = 59.662123


def buss(lon=LON, lat=LAT):
    lon = lon

    try:
        conn = psycopg2.connect(dbname='master', user='postgres',
        password='', host='localhost', port=5432)
    except ValueError:
        print('database ikke tilkoblet')

    sql = ("""with index_query as (
    select ST_Distance(
    geom ::geography,
    ST_POINT({}, {}) ::geography) as distance,
    ST_DWithin(st_buffer(geom ::geography, 7), ST_POINT({}, {})  ::geography, 10) as t, type as type 
    from n50.jernbane
        order by geom <-> ST_POINT({}, {}) limit 100
)
select distance, t, type from index_query order by distance limit 1
""").format(lon, lat, lon, lat, lon, lat)

    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return (rows[0])

if __name__ == "__main__":
    print(buss(10,59))