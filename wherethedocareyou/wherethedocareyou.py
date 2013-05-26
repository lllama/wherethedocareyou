# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
from urlparse import urlparse

import flask
import os
import pymongo

app = flask.Flask(__name__)

x = 500
y = 430

MONGO_URL = os.environ['MONGOHQ_URL']
mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client[urlparse(MONGO_URL).path[1:]]
locations = db['locations']

@app.route("/whereami")
def whereami():
    return coordinates()

@app.route("/location/me")
def coordinates():
    # Sick hackery...
    import random
    global x, y
    x += random.randint(-10, 10)
    y += random.randint(-10, 10)
    return flask.jsonify({'x': x, 'y': y})

@app.route("/")
def home():
    return ""

@app.route("/map")
def map():
    return flask.render_template("map.html")

@app.route("/badger", methods=['POST'])
def badger():
    # Because why would I name the function sensibly or provide useful output?
    print(str(flask.request.json))
    map_data = db['map_data']
    map_data.insert(flask.request.json)
    return ""

@app.route("/location/me/update", methods=['POST'])
def update_location():
    # Because hacks, that's why!
    me = flask.request.json
    me['user'] = "me"
    locations.insert(me)
    maths() #I'm so sorry
    return ""

def maths():
    # I sicken me
    me = locations.find_one({'user': 'me'})
    if not me:
        return

    # What's that you say? Dumb+hacky n-dimensional nearest neighbour? Why yes!
    distances = []
    for map_datum in map_data.find():
        map_datum_locations = map_datum['locations']
        def f(bssid):
            for map_ap in map_datum_locations:
                if map_ap['BSSID'] == bssid:
                    return map_ap
        d = 0
        for ap in me['locations']:
            BSSID = ap['BSSID']
            map_ap = f(BSSID)
            d += abs(abs(ap['level']) - abs(map_ap['level']))
        distances += {'map_datum': map_datum._id, 'distance': d}

    print(distances)

    sorted(distances, key=lambda x: x['distance'])

    nearest_ap = distances[0]
    nearest_BSSID = nearest_ap['BSSID']

    print(nearest_BSSID)

    #TODO Poke this when we have more data



if __name__ == "__main__":
    PORT = int(os.getenv('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
