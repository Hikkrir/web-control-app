from flask import Flask, Response, render_template, jsonify

from servo_motor_handler import Control
# from img_processing.video_stream import video_generator
from img_processing.road_detection import RoadDetection

control_handler = Control()
road = RoadDetection()
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
    return Response(road.get_frame_with_curve_result(automode= mode), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/keyboard_control_speed/<speed>", methods=['POST', 'GET'])
def keyboard_control_speed(speed):
    control_handler.move_backward(speed) if int(speed) < 0 else control_handler.move_forward(speed)
    return jsonify(True)

@app.route("/keyboard_control_angle/<angle>", methods=['POST', 'GET'])
def keyboard_control_angle(angle):
    control_handler.change_angle_servo(angle)
    return jsonify(True)

with open('check.txt', 'w') as file:
    file.write("false")
app.run(debug=False, host="0.0.0.0", port=8888)