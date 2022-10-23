from flask import Flask, Response, render_template, jsonify

from servo_motor_handler import Control
from img_processing.video_stream import video_generator

control_handler = Control()
app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def main_page():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/keyboard_control_speed/<speed>", methods=['POST', 'GET'])
def keyboard_control_speed(speed):
    control_handler.move_backward(speed) if int(speed) < 0 else control_handler.move_forward(speed)
    return jsonify(True)

@app.route("/keyboard_control_angle/<angle>", methods=['POST', 'GET'])
def keyboard_control_angle(angle):
    control_handler.change_angle_servo(angle)
    return jsonify(True)

app.run(debug=False, host="0.0.0.0", port=8888)