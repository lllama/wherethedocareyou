# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import flask
import os

app = flask.Flask(__name__)

@app.route("/whereami")
def coordinates():
    return flask.jsonify({'x': 0, 'y': 0})

@app.route("/")
def home():
    return ""

@app.route("/map")
def map():
    return flask.render_template("map.html")

if __name__ == "__main__":
    PORT = int(os.getenv('PORT', 5000))
    app.debug = True
    app.run(port=PORT)
