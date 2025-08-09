from flask import Flask, render_template, Response, request, redirect, url_for
from pose_left import left_curl
from pose_right import right_curl
from pose_pushup import pushup
from pose_squat import squat
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api', methods=['GET'])
def index():
    return redirect(url_for('home'))

@app.route('/video_feed_left')
def video_feed_left():
    return Response(left_curl(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_right')
def video_feed_right():
    return Response(right_curl(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_pushup')
def video_feed_pushup():
    return Response(pushup(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_squat')
def video_feed_squat():
    return Response(squat(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/show')
def show():
    subject = request.args.get('sub', '').strip().lower()
    allowed = {'left', 'right', 'pushup', 'squat'}
    if subject not in allowed:
        return redirect(url_for('home'))
    return redirect(f'/video_feed_{subject}')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)