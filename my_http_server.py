#!/usr/bin/env python3

import os
try:
    from flask import Flask,request,abort
except:
    os.system("pip3 install flask")
    from flask import Flask,request,abort
import requests, json
from Mongodb import DB
app = Flask(__name__)
settings = None

#API 4
@app.route('/popularsearch')
def get_popularsearch():
    if not database.is_connect:
        database(DB(settings))
    info = database.get_max_hits()
    if info == None:
        abort(500)
    return {"source": info["location_1"], "destination": info["location_2"], "hits": info["hits"]}

#API 3
@app.route('/health')
def get_health():
    if not database.is_connect:
        abort(500)
    return ""

#API 1
@app.route('/hello')
def get_hello():
    return ''

#API 2
@app.route('/distance' , methods=['GET', 'POST'])
def get_distance():
    if request.method == 'POST':
        if not database.is_connect:
            database(DB(settings))
        info = database.update(eval(request.data))
        return info, 201
    if request.method == 'GET':
        if not database.is_connect:
            database(DB(settings))
        source = request.args.get('source')
        destination = request.args.get('destination')
        try:
            info_from_db = database.find_distances_by_locations(source, destination)
        except Exception as e:
            info_from_db = None
        if info_from_db == None:
            info = get_distance_from_api(source,destination, settings["google_api_key"])#'AIzaSyAGAxX_AOF4ykkXzooia1DYHfvnnmv1eGU'
            if info["rows"][0]["elements"][0]["status"] != "OK":
                return ""
            dest = info["rows"][0]["elements"][0]["distance"]["text"]
            database.insert(destination, source, dest)
            return {"distance": dest}

        else:
            return {"distance":  info_from_db["distance"]}




def get_distance_from_api(source, dest, key):

    api_key = key
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'


    r = requests.get(url + 'origins=' + source +
                     '&destinations=' + dest +
                     '&key=' + api_key)
    info = r.json()
    return info


if __name__ == '__main__':
    from sys import argv
    print(argv[0])
    from pathlib import Path
    path = argv[0][0:argv[0].find(Path(__file__).name)]
    with open(path+'settings.json') as f:
        settings = json.load(f)
    _port = 8080
    _host = '127.0.0.1'
    if len(argv) >= 2:
        _port = int(argv[1])
    if len(argv) >= 3:
        _host = argv[2]
    database = DB(settings)
    app.run(debug=True, port=_port, host=_host)
