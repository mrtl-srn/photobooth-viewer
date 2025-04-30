import eventlet  # noqa
eventlet.monkey_patch()  # noqa

from threading import Thread
from flask_socketio import SocketIO
from flask import Flask, send_from_directory, render_template, request
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
import socket
import time

load_dotenv()
PHOTO_FOLDER = os.getenv("PHOTO_FOLDER")
PHOTO_EXTENSIONS = os.getenv("PHOTO_EXTENSIONS", ".jpg").split(",")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", 2))

if not PHOTO_FOLDER:
    raise ValueError("PHOTO_FOLDER environment variable is not set.")
if not os.path.exists(PHOTO_FOLDER):
    raise ValueError(f"PHOTO_FOLDER does not exist: {PHOTO_FOLDER}")
if not os.path.isdir(PHOTO_FOLDER):
    raise ValueError(f"PHOTO_FOLDER is not a directory: {PHOTO_FOLDER}")
if not os.access(PHOTO_FOLDER, os.R_OK):
    raise ValueError(f"PHOTO_FOLDER is not readable: {PHOTO_FOLDER}")


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='eventlet', logger=DEBUG, engineio_logger=DEBUG)
last_sent = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/photos/<filename>')
def get_photo(filename):
    return send_from_directory(PHOTO_FOLDER, secure_filename(filename))


@socketio.on('connect')
def handle_connect():
    print("✅ New client connected")
    if last_sent:
        print(f"➡️ Sending the last photo : {last_sent}")
        socketio.emit('new_photo', {'filename': last_sent}, to=request.sid)
    else:
        print("➡️ No files found, sending default image")
        socketio.emit('new_photo', {'filename': 'static/default.jpg'}, to=request.sid)


def is_valid_photo(filename):
    return any(filename.lower().endswith(ext) for ext in PHOTO_EXTENSIONS)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "localhost"
    return ip


def watch_folder():
    global last_sent
    while True:
        try:
            files = sorted(
                [f for f in os.listdir(PHOTO_FOLDER) if os.path.isfile(
                    os.path.join(PHOTO_FOLDER, f)) and is_valid_photo(f)],
                key=lambda x: os.path.getmtime(os.path.join(PHOTO_FOLDER, x))
            )
            if files:
                latest = files[-1]
                if latest != last_sent:
                    last_sent = latest
                    print("📤 Sending : ", latest)
                    socketio.emit('new_photo', {'filename': latest})
        except Exception as e:
            print(f"[watch_folder error] {e}")
        time.sleep(SCAN_INTERVAL)


# Start monitoring in a separate thread
Thread(target=watch_folder, daemon=True).start()

if __name__ == '__main__':
    loopback = "127.0.0.1"
    host_ip = get_local_ip()

    print("\n🌐 Web interface available at:")
    print(f"🔁 Loopback     → http://{loopback}:{PORT}")
    print(f"🖥️  Host local  → http://{host_ip}:{PORT}")

    socketio.run(app, host=HOST, port=int(PORT))
