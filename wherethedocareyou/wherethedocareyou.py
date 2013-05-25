# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import flask
import os

app = flask.Flask(__name__)

x = 10
y = 10

@app.route("/whereami")
def coordinates():
    # Sick hackery...
    import random
    global x, y
    x += random.randint(-1, 1)
    y += random.randint(-1, 1)
    return flask.jsonify({'x': x, 'y': y})

@app.route("/")
def home():
    return ""

@app.route("/map")
def map():
    return flask.render_template("map.html")

@app.route("/badger", methods=['POST'])
def badger():
    print(str(flask.request.json))
    return ""

if __name__ == "__main__":
    PORT = int(os.getenv('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
