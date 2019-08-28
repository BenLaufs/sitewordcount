import os
import requests, json

from flask import Flask, jsonify, render_template, request, url_for
from flask_socketio import SocketIO, emit
from processing import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

@app.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html")

@socketio.on("search")
def search_trigger(data):
    print("recieved")
    searchword = data["searchword"]
    baseurl = data["baseurl"]
    urls = readUrlConfig(baseurl)
    l = len (urls)
    n = 0
    urls_searched = 0
    for u in urls:
        i = 0
        urls_searched = urls_searched + 1
        try:
            i = process(u, searchword)
            print(i)
            if i != "#":
                n = n + i
                web_data = {'total_urls': l, 'searchword': searchword, 'total_hits': n, 'urls_searched': urls_searched, 'url': u, 'hits': i}
                emit("show results", web_data, broadcast=True)
                socketio.sleep(1)
        except:
            continue
