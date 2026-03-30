from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import yt_dlp
import os
import tempfile
import threading
import uuid

app = Flask(__name__)
CORS(app)

# Track download progress
progress_store = {}

HTML = open("index.html").read() if os.path.exists("index.html") else ""

def download_video(url, fmt, job_id, output_dir):
    progress_store[job_id] = {"status": "downloading", "percent": 0, "filename": None, "error": None}

    def progress_hook(d):
        if d["status"] == "downloading":
            pct = d.get("_percent_str", "0%").strip().replace("%", "")
            try:
                progress_store[job_id]["percent"] = float(pct)
            except:
                pass
        elif d["status"] == "finished":
            progress_store[job_id]["status"] = "finished"
            progress_store[job_id]["percent"] = 100
            progress_store[job_id]["filename"] = d["filename"]

    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
    }

    if fmt == "mp3":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    elif fmt == "mp4_720":
        ydl_opts["format"] = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    elif fmt == "mp4_1080":
        ydl_opts["format"] = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    else:
        ydl_opts["format"] = "best"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        progress_store[job_id]["status"] = "error"
        progress_store[job_id]["error"] = str(e)


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/info", methods=["POST"])
def get_info():
    data = request.json
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get("title", "Unknown"),
                "thumbnail": info.get("thumbnail", ""),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "Unknown"),
                "platform": info.get("extractor_key", "Unknown"),
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download", methods=["POST"])
def start_download():
    data = request.json
    url = data.get("url", "").strip()
    fmt = data.get("format", "best")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    job_id = str(uuid.uuid4())
    output_dir = tempfile.mkdtemp()

    thread = threading.Thread(target=download_video, args=(url, fmt, job_id, output_dir))
    thread.daemon = True
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/progress/<job_id>")
def check_progress(job_id):
    info = progress_store.get(job_id)
    if not info:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(info)


@app.route("/file/<job_id>")
def serve_file(job_id):
    info = progress_store.get(job_id)
    if not info or info.get("status") != "finished":
        return jsonify({"error": "File not ready"}), 404

    filepath = info.get("filename")
    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "File missing"}), 404

    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
