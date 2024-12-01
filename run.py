import json
import os.path

from analyzer import analyze
from ProjectExceptions import *

import logging

from flask import Flask, request, Response, render_template_string
from flask_cors import CORS

import yt_dlp
import validators

from chatgpt import generateSummary, generate_true_false

app = Flask(__name__)
CORS(app)

TARGET_FILE: str = None

video_db = {}
if os.path.isfile("./data/video_db.json"):
    with open("./data/video_db.json", "r") as f:
        video_db = json.load(f)
else:
    with open("./data/video_db.json", "w") as f:
        json.dump(video_db, f)


def download_video(video_url: str):
    # Remove unnecessary params
    pos = video_url.find("&")
    if pos != -1:
        video_url = video_url[0:pos]

    # Download the video
    global TARGET_FILE
    print(video_url)
    if video_url in video_db:
        TARGET_FILE = video_db[video_url]
    else:
        opt = {
            "outtmpl": {}
        }
        with yt_dlp.YoutubeDL(opt) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info['title']
            proc_title = "".join(filter(str.isalpha, title))
            video_db[video_url] = proc_title
            print(proc_title)
            ydl.params['outtmpl']['default'] = f'./data/{proc_title}.mp4'
            ydl.download(video_url)

        with open(f"./data/video_db.json", "w") as f:
            json.dump(video_db, f, indent=4)

        TARGET_FILE = video_db[video_url]

    return TARGET_FILE


@app.route("/upload", methods=['POST'])
def upload():
    lnk = request.form.get("link")
    print(lnk)
    print(request.form)
    f_name = download_video(lnk)
    response = Response()
    response.status_code = 200
    response.data = json.dumps({"file_name": f_name})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/')
def home():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>YouTube Video Analyzer</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #555;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 16px;
                box-sizing: border-box;
            }
            .button-group {
                display: flex;
                gap: 10px;
                justify-content: center;
            }
            button {
                padding: 12px 24px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #0056b3;
            }
            .analyze-btn {
                background-color: #28a745;
            }
            .analyze-btn:hover {
                background-color: #218838;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>YouTube Video Analyzer</h1>
            <div class="form-group">
                <label for="vidURL">Enter YouTube URL:</label>
                <input type="text" id="vidURL" name="vidURL" placeholder="https://www.youtube.com/watch?v=...">
            </div>
            <div class="button-group">
                <button onclick="watchVideo()">Watch Video</button>
            </div>
        </div>

        <script>
            function watchVideo() {
                const url = document.getElementById('vidURL').value;
                if (!url) {
                    alert('Please enter a YouTube URL');
                    return;
                }
                
                const formData = new FormData();
                formData.append('vidURL', url);
                
                fetch('/video', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.text())
                .then(html => {
                    document.body.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error processing video');
                });
            }

            function analyzeVideo() {
                // You can implement video analysis functionality here
                alert('Analysis feature coming soon!');
            }
        </script>
    </body>
    </html>
    """
    response = Response(html_template, status=200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/video", methods=['POST'])
def watch_video():
    vidURL = request.form.get("vidURL")

    # CASE 0: URL not entered in.
    if not vidURL:
        response = Response("No yt video URL provided", status=400)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    # CASE 1: Invalid URL.
    if not validators.url(vidURL):
        response = Response("Invalid URL format", status=400)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    # CASE 2: Valid URL.
    try:
        # Configure yt-dlp
        ydl_opts = {
            'format': 'best',
            'extract_flat': True,
        }

        # Extract video information
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(vidURL, download=False)

        # Get video details
        video_title = info.get('title', 'Video')
        video_id = info.get('id', '')

        if 'youtube.com' in vidURL or 'youtu.be' in vidURL:
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>{{ video_title }}</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                    .video-container {
                        position: relative;
                        width: 100%;
                        padding-bottom: 56.25%;
                        height: 0;
                        background-color: white;
                        border-radius: 10px;
                        overflow: hidden;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }
                    .video-container iframe {
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                    }
                    .back-button {
                        display: inline-block;
                        margin: 20px 0;
                        padding: 12px 24px;
                        background-color: #007bff;
                        color: white;
                        text-decoration: none;
                        border-radius: 4px;
                        transition: background-color 0.3s;
                    }
                    .back-button:hover {
                        background-color: #0056b3;
                    }
                    h1 {
                        color: #333;
                        margin-bottom: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{{ video_title }}</h1>
                    <div class="video-container">
                        <iframe 
                            src="https://www.youtube.com/embed/{{ video_id }}"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen>
                        </iframe>
                    </div>
                    <a href="/" class="back-button">Back to Home</a>
                </div>
            </body>
            </html>
            """

            response = render_template_string(
                html_template,
                video_title=video_title,
                video_id=video_id
            )
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

        else:
            response = Response("Only YouTube videos are supported at this time", status=400)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

    except Exception as e:
        logging.error(f"Error processing video: {str(e)}")
        response = Response(f"Error processing video: {str(e)}", status=500)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


@app.route("/transcript", methods=['POST'])
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
        response.data = json.dumps(res)
        response.status_code = 200
    except VideoNotFound:
        response.data = "No video uploaded"
        response.status_code = 502

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/summary", methods=['GET'])
def summary():
    res = generateSummary(f"{TARGET_FILE}", raw=False)
    response = Response()
    response.data = json.dumps(res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/quiz", methods=['GET'])
def quiz():
    res = generate_true_false(f"{TARGET_FILE}")
    response = Response()
    response.data = json.dumps(res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=20000)
