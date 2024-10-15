import logging

from flask import Flask, request, Response
from flask_cors import CORS

from analyzer import analyze
from ProjectExceptions import *

app = Flask(__name__)
CORS(app)

TARGET_FILE: str = None


@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route("/upload", methods=['POST'])
def upload():
    global TARGET_FILE
    file = request.form.get("filename")
    ext = request.form.get("ext")
    TARGET_FILE = f"{file}.{ext}"
    return "Success"


@app.route("/download", methods=['POST'])
def download():
    get_raw = request.form.get("raw")
    if get_raw.lower() == "false":
        get_raw = False
    else:
        get_raw = True
    response = Response()
    if TARGET_FILE and TARGET_FILE is None:
        logging.warning("File not selected")
    try:
        res = analyze(TARGET_FILE, raw=get_raw)
        response.data = str(res)
        response.status_code = 200
    except VideoNotFound:
        response.data = "No video uploaded"
        response.status_code = 502

    return response


app.run(host="0.0.0.0", port=20000)
