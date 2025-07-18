# web/app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import queue
import threading
import subprocess
import logging
from config import HISTORY_PATH, PROJECTS_PATH
import json
from flask import send_from_directory

app = Flask(__name__)
socketio = SocketIO(app)
task_queue = queue.Queue()

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline_worker():
    while True:
        topic = task_queue.get()
        socketio.emit("status", {"status": f"🚀 Running: {topic}"})
        try:
            result = subprocess.run(
                ["python3", "-u", "run_recursive_pipeline.py", topic],
                capture_output=True,
                text=True,
                env={"RESEARCH_TOPIC": topic}
            )
            status = f"✅ Complete: {topic}\n{result.stdout}" if result.returncode == 0 else f"❌ Failed: {result.stderr}"
            socketio.emit("status", {"status": status})
            logging.info(status)
        except Exception as e:
            status = f"❌ Exception: {e}"
            socketio.emit("status", {"status": status})
            logging.error(status)
        task_queue.task_done()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"].strip()
        if not topic:
            return render_template("index.html", error="Please enter a valid topic.")
        if len(topic) > 100:
            return render_template("index.html", error="Topic too long (max 100 characters).")
        task_queue.put(topic)
        return redirect(url_for("status"))
    return render_template("index.html")

@app.route("/status")
def status():
    return render_template("status.html")

@app.route("/dashboard")
def dashboard():
    projects = []
    try:
        with open(HISTORY_PATH, "r") as f:
            for line in f:
                try:
                    projects.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return render_template("dashboard.html", projects=projects[::-1])

@app.route("/projects/<path:filename>")
def serve_project_file(filename):
    return send_from_directory(PROJECTS_PATH, filename)

if __name__ == "__main__":
    threading.Thread(target=run_pipeline_worker, daemon=True).start()
    socketio.run(app, debug=True)