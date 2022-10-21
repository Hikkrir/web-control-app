import json

import cv2 as cv
from flask import Flask, Response, render_template

app = Flask(__name__, template_folder="D:\web_app\\templates\\", static_folder="D:\web_app\static\\")

@app.route("/video_generator")
def video_generator():
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH , 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        ret, frame = cap.read()
        if ret:
            _, buffer = cv.imencode('.jpg', frame)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route("/")
def main_page():
    return render_template('index.html' )

@app.route('/video_feed')
def video_feed():
    return Response(video_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/keyboard_control/<keyEvent>", methods=['POST', 'GET'])
def keyboard_control(keyEvent):
    if keyEvent == 's':
        print("S PRESSED")
    if keyEvent == 'w':
        print("W PRESSED")
    if keyEvent == 'a':
        print("A PRESSED")
    if keyEvent == 'd':
        print("D PRESSED")
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

app.run(debug=False, host="0.0.0.0", port=8888)