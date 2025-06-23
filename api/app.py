from flask import Flask, send_file
import os
import glob

app = Flask(__name__)


@app.route("/latest_sunset")
def get_latest():
    latest = max(glob.glob("/opt/sunset_archive/*.jpg"), key=os.path.getctime)
    return send_file(latest, mimetype="image/jpeg")
