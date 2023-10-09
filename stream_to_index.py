from flask import Flask, render_template, Response, request
import cv2
import data
import os

# make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

# instatiate flask app
app = Flask(__name__, template_folder='./templates', static_url_path='/custom_static', static_folder='static')

camera = cv2.VideoCapture(0)


def gen_frames():  # generate frame by frame from camera
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


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
