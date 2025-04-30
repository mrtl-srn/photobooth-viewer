# 📸 Photobooth Viewer

A lightweight web application for Raspberry Pi (or any host) that automatically displays the latest photo from a watched folder. Perfect for events and parties with a self-service photobooth.


## 🚀 Features

- 🔄 Real-time folder monitoring
- 🖼️ Automatically shows the latest photo taken
- ⚡ Instant updates via WebSocket (no page reload)
- 🌐 Accessible via local network (loopback, host IP, container IP)
- 🛠️ Configurable via `.env` file
- 🖼️ Fallback image shown if no photo is available


## 🧰 Tech Stack

- Python 3
- Flask + Flask-SocketIO
- Eventlet
- dotenv
- HTML / JavaScript (WebSocket frontend)


## 🔧 Configuration

Create a `.env` file at the root of the project with:

```env
# Folder containing your photos
PHOTO_FOLDER=/path/to/your/photo/folder

# Supported photo extensions
PHOTO_EXTENSIONS=.jpg,.jpeg,.png

# Interval (in seconds) between folder scans
SCAN_INTERVAL=2

# Server host and port
HOST=0.0.0.0
PORT=5000

# Debug mode (True or False)
DEBUG=False
```

## 🚀 Run the App

### Locally:
```bash
pip install -r requirements.txt
python app.py
```

### In Docker (optional):

```bash
docker build -t photobooth-viewer .
docker run -p 5000:5000 -v /your/photo/folder:/photos photobooth-viewer
```

## 🌐 Access the Web App

When launched, the app prints all available local URLs:

```
🌐 Web interface available at:
🔁 Loopback     → http://127.0.0.1:5000
🖥️ Host local   → http://192.168.1.42:5000
```

## 📁 Project Structure

```
photobooth-viewer/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── default.jpg
├── .env
├── requirements.txt
└── README.md
```

## 📜 License

MIT – Free to use and modify for personal or community projects.