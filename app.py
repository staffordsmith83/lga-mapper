# app.py
from flask import Flask, request, jsonify, abort
import utils.spatial_analysis as sa
import os
import psycopg2
import json
from geojson import loads, Feature, FeatureCollection
from flask_cors import CORS

# app = Flask('rpg_flask_api')
app = Flask(__name__)

# TODO: Check this Disables CORS for production
# if os.environ['FLASK_ENV'] != 'prod':
#     CORS(app)
CORS(app)

# setup DB connection


def get_db_connection(database):
    conn = psycopg2.connect(
        host="localhost",
        database=database,
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    return conn

##########################
# DB ENDPOINTS
##########################

@app.route("/lgas", methods=['GET'])
def get_lgas():
    database = 'postgres'
    conn = get_db_connection(database)
    cur = conn.cursor()

    if request.method == 'GET':
        sql = """ SELECT councilnam,
        ST_AsGeoJSON(ST_Transform(geom,4326)) AS geom
        FROM api.lgas LIMIT 5;  """

        cur.execute(sql)
        # return all the rows, we expect more than one
        db_rows = cur.fetchall()
        cur.close()
        conn.close()


        return export2geojson(db_rows)


# The the first LGA that intersects with the provided lat and lng, and return the name and abscode as json.
@app.route("/lga", methods=['GET'])
def get_lga():
    database = 'postgres'
    conn = get_db_connection(database)
    cur = conn.cursor()

    app.logger.info("Finding LGA from coordinates")
    args = request.args.to_dict()
    lat = args.get('lat')
    lng = args.get('lng')

    sql = f'SELECT councilnam, abscode FROM api.lgas WHERE ST_Intersects(geom, ST_SetSRID(ST_MakePoint({lng}, {lat}), 4326)); '
    'VALUES (%s, %s)',
    (lat, lng)

    cur.execute(sql)

    db_rows = cur.fetchall()
    cur.close()
    conn.close()
    result = {
        'name': db_rows[0][0],
        'abscode': db_rows[0][1]
    }

    return result


# Modified from https://subscription.packtpub.com/book/big-data-and-business-intelligence/9781783555079/4/ch04lvl1sec34/finding-out-whether-a-point-is-inside-a-polygon


def export2geojson(db_rows):
    print(db_rows)
    """
    loop through each row in result query set and add to my feature collection
    assign name field to the GeoJSON properties
    :param query_result: pg query set of geometries
    :return: new geojson file
    """
    # an empty list to hold each feature of our feature collection
    new_geom_collection = []

    for row in db_rows:
        name = row[0]
        geom = row[1]
        geoj_geom = loads(geom)
        myfeat = Feature(geometry=geoj_geom,
                         properties={'name': name})
        new_geom_collection.append(myfeat)

    # use the geojson module to create the final Feature
    # Collection of features created from for loop above
    my_geojson = FeatureCollection(new_geom_collection)

    return my_geojson


def query_db(database, query, args=(), one=False):
    conn = get_db_connection(database)
    cur = conn.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    # cur.close()
    # conn.close()
    return (r[0] if r else None) if one else r

