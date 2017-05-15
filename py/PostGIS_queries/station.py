import psycopg2

LON = 10.787869
LAT = 59.662123

def stasjoner(lon=LON, lat=LAT):
    lon = lon
    lat = lat

    try:
        conn = psycopg2.connect(dbname='master', user='postgres',
        password='', host='localhost', port=5432)
    except ValueError:
        print('database ikke tilkoblet')

    sql = ("""with index_query as (
    select ST_Distance(
    geom ::geography,
    ST_POINT({}, {}) ::geography) as distance,
    ST_DWithin(st_buffer(geom ::geography, 10), ST_POINT({}, {})  ::geography, 10) as t, type as type, gid as id
    from n50.stasjoner
        order by geom <-> ST_POINT({}, {}) limit 100
)
select distance, id, t, type from index_query order by distance limit 1
""").format(lon, lat, lon, lat, lon, lat)

    sql2 = ("""with index_query as (
    select ST_Distance(
    wkb_geometry ::geography,
    ST_POINT({}, {}) ::geography) as distance,
    ST_DWithin(st_buffer(wkb_geometry ::geography, 10), ST_POINT({}, {})  ::geography, 10) as t, bus as type, ogc_fid as id
    from n50.stasjoner2
        order by wkb_geometry <-> ST_POINT({}, {}) limit 100
)
select distance, id, t, type from index_query order by distance limit 1
""").format(lon, lat, lon, lat, lon, lat)

    cursor = conn.cursor()
    cursor.execute(sql2)
    rows = cursor.fetchall()
    return rows[0]

if __name__ == "__main__":
    # print(sql(10,59))
    pass
