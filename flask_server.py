from threading import Thread
from flask import Flask, Response, render_template, jsonify

from servo_motor_handler import Control
from img_processing.road_detection import RoadDetection

control_handler = Control()
video_stream = RoadDetection()
Thread(target= video_stream.automode, name= "automode").start()
app = Flask(__name__, template_folder="templates", static_folder="static")
mode = False

@app.route("/")
def main_page():
    return render_template('index.html')

@app.route("/check_mode/<automode>", methods=['POST', 'GET'])
def check_mode(automode):
    control_handler.change_angle_servo(110)
    control_handler.move_forward(0)
    with open('check.txt', 'w') as file:
        file.write(automode)
    return jsonify(True)

@app.route('/video_feed')
def video_feed():
    return Response(video_stream.video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/keyboard_control_speed/<speed>", methods=['POST', 'GET'])
def keyboard_control_speed(speed):
    speed = int(speed)
    # if speed == 0:
    #     control_handler.stop()
    #     return jsonify(True)
    # elif speed < 0:
    #     control_handler.move_backward(abs(speed))
    #     return jsonify(True)
    # else:
    #     control_handler.move_forward(abs(speed))
    return jsonify(True)

@app.route("/keyboard_control_angle/<angle>", methods=['POST', 'GET'])
def keyboard_control_angle(angle):
    control_handler.change_angle_servo(int(angle))
    return jsonify(True)

app.run(debug=False, host="0.0.0.0", port=8888)