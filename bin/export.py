#!/usr/bin/env python

import os
import sys
import logging
import geojson

import shapely.geometry

import mapzen.whosonfirst.utils
import mapzen.whosonfirst.geojson

if __name__ == '__main__':

    f = sys.argv[1]

    print "load %s" % f

    fh = open(f, 'r')

    data = geojson.load(fh)

    m = {
        "woe_id": "woe:id",
        "place_id": "woe:place_id",
        "place_type": "woe:placetype",
        "place_type_id": "woe:placetype_id",
        "label": "woe:name",
        }

    for ftr in data['features']:

        props = ftr['properties']

        for k, v in props.items():

            if m.get(k, False):

                props[m[k]] = v
                del(props[k])

        props['placetype'] = props['woe:placetype']
        props['name'] = props['woe:name']

        ftr['properties'] = props

        shp = shapely.geometry.asShape(ftr['geometry'])
        ftr['bbox'] = shp.bounds

        id = ftr['id']

        path = mapzen.whosonfirst.utils.id2path(id)
        path = os.path.join("../data", path)
        path = os.path.abspath(path)

        if not os.path.exists(path):
            os.makedirs(path)

        fname = "%s.geojson" % id
        path = os.path.join(path, fname)

        print "write %s" % path

        out = open(path, "w")

        e = mapzen.whosonfirst.geojson.encoder()
        e.encode_feature(ftr, out)
        
    
