""" 
Module of useful spatial analysis functions to be used in the api.
Neater to keep this separate, and may be useful in other applications
"""


from shapely.geometry import shape, mapping
import json


def get_centroids(polygons_json):

    feature_collection = {
        'type': 'FeatureCollection',
        'features': []
    }

    for feature in json.loads(polygons_json)['features']:
        feature_geom = shape(feature['geometry'])
        feature_centroid = feature_geom.centroid
        centroid = mapping(feature_centroid)
        feature['geometry'] = centroid
        feature_collection['features'].append(feature)

    return feature_collection

