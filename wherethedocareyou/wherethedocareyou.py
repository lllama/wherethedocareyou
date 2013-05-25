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
    locations = db['locations']
    locations.insert(flask.request.json)
    return ""

if __name__ == "__main__":
    PORT = int(os.getenv('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
