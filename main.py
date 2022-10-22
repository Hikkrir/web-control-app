import json

import cv2 as cv
from flask import Flask, Response, render_template

from img_processing.video_stream import video_generator

app = Flask(__name__, template_folder=".\\templates\\", static_folder=".\static\\")

@app.route("/")
def main_page():
    return render_template('index.html' )

@app.route('/video_feed')
def video_feed():
    return Response(video_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/keyboard_control_speed/<speed>", methods=['POST', 'GET'])
def keyboard_control_speed(speed):
    print(f"current speed [ {speed} ]")
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route("/keyboard_control_angle/<angle>", methods=['POST', 'GET'])
def keyboard_control_angle(angle):
    print(f"current angle [ {angle} ]")
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}  

app.run(debug=False, host="0.0.0.0", port=8888)