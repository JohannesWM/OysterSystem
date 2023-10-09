from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
import threading
import cv2
import data
import os

try:
    os.mkdir('./shots')
except OSError as error:
    pass

app = Flask(__name__, template_folder='./templates', static_url_path='/custom_static', static_folder='static')
socketio = SocketIO(app)

lock = threading.Lock()
locked = False

camera = cv2.VideoCapture(0)


def gen_frames():
    while True:
        success, frame = camera.read()

        if success:
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass


@app.route('/')
def index():
    return render_template('index.html',
                           data=data.get(), log=data.fetch())


@app.route('/log')
def log():
    return render_template('log.html',
                           logAll=data.fetchAll())


@app.route('/stream')
def stream():
    global locked
    if not locked:
        with lock:
            locked = True
            return render_template('stream.html')
    else:
        return "Someone is already watching the stream. Please try again later."


@socketio.on('disconnect')
def handle_disconnect():
    global locked
    locked = False


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
