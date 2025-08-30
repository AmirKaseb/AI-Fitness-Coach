from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
from pose_left import left_curl
from pose_right import right_curl
from pose_pushup import pushup
from pose_squat import squat
import cv2
import mediapipe as mp
import numpy as np
import os
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

app = Flask(__name__, static_folder='static')

# Global variables for demo mode
demo_mode = False
demo_exercise = None

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

@app.route('/api/exercise/<exercise_type>')
def get_exercise_info(exercise_type):
    """API endpoint to get exercise information"""
    exercise_data = {
        'left': {
            'name': 'Left Arm Curl',
            'target': 12,
            'description': 'Build strong biceps with proper form',
            'tips': ['Keep your back straight', 'Control the movement', 'Feel the burn in your biceps']
        },
        'right': {
            'name': 'Right Arm Curl',
            'target': 12,
            'description': 'Build strong biceps with proper form',
            'tips': ['Keep your back straight', 'Control the movement', 'Feel the burn in your biceps']
        },
        'pushup': {
            'name': 'Push-ups',
            'target': 10,
            'description': 'Full body strength exercise',
            'tips': ['Keep your body straight', 'Lower your chest to the ground', 'Push up with control']
        },
        'squat': {
            'name': 'Squats',
            'target': 15,
            'description': 'Leg power and strength builder',
            'tips': ['Keep your back straight', 'Go as low as you can', 'Push through your heels']
        }
    }
    
    if exercise_type in exercise_data:
        return jsonify(exercise_data[exercise_type])
    else:
        return jsonify({'error': 'Exercise not found'}), 404

@app.route('/api/demo/start')
def start_demo():
    """Start demo mode"""
    global demo_mode
    demo_mode = True
    return jsonify({'status': 'success', 'message': 'Demo mode started'})

@app.route('/api/demo/stop')
def stop_demo():
    """Stop demo mode"""
    global demo_mode
    demo_mode = False
    return jsonify({'status': 'success', 'message': 'Demo mode stopped'})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Backend is running'})

@app.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # For demo purposes, accept any login
        # In production, you would validate against a database
        if email and password:
            return jsonify({
                'id': 1,
                'name': 'Demo User',
                'email': email,
                'status': 'success'
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    try:
        data = request.get_json()
        fullname = data.get('fullname')
        email = data.get('email')
        password = data.get('password')
        
        # For demo purposes, accept any signup
        # In production, you would save to a database
        if fullname and email and password:
            return jsonify({
                'id': 1,
                'name': fullname,
                'email': email,
                'status': 'success'
            })
        else:
            return jsonify({'error': 'Missing required fields'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/profile', methods=['POST'])
def profile():
    """User profile setup endpoint"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        birthdate = data.get('birthdate')
        name = data.get('name')
        gender = data.get('gender')
        
        # For demo purposes, accept any profile
        # In production, you would save to a database
        if user_id and name:
            return jsonify({
                'id': user_id,
                'name': name,
                'birthdate': birthdate,
                'gender': gender,
                'status': 'success'
            })
        else:
            return jsonify({'error': 'Missing required fields'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    # Check if running in production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🏋️‍♀️ GymJam AI Fitness Coach Starting...")
    print(f"🌐 Server running on port {port}")
    print("📱 Open your browser and navigate to the frontend")
    print("🎯 Features: Real-time pose detection, form feedback, progress tracking")
    
    app.run(host="0.0.0.0", port=port, debug=debug)