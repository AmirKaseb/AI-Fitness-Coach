"""
GymJam AI - WebRTC Backend Server
Clean, production-ready Flask-SocketIO application
"""

from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import cv2
import mediapipe as mp
import numpy as np
import os
import base64
import io
from PIL import Image

# Import clean WebRTC exercise modules
from exercises.pushup_webrtc import process_pushup_frame
from exercises.left_curl_webrtc import process_left_curl_frame
from exercises.right_curl_webrtc import process_right_curl_frame
from exercises.squat_webrtc import process_squat_frame

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gymjam-ai-secret-key-2024')
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for WebRTC processing
active_sessions = {}

@app.route('/')
def home():
    """Serve the main application page"""
    return render_template('home.html')

@app.route('/health')
def health_check():
    """Health check endpoint for cloud deployment"""
    return jsonify({
        'status': 'healthy', 
        'message': 'GymJam AI WebRTC Backend is running',
        'active_sessions': len(active_sessions),
        'version': '1.0.0'
    })

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

# WebSocket event handlers for WebRTC
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to GymJam AI WebRTC Server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")
    if request.sid in active_sessions:
        del active_sessions[request.sid]

@socketio.on('start_exercise')
def handle_start_exercise(data):
    """Start exercise session"""
    exercise_type = data.get('exercise_type')
    session_id = request.sid
    
    active_sessions[session_id] = {
        'exercise_type': exercise_type,
        'count': 0,
        'calories': 0,
        'form_score': 0
    }
    
    emit('exercise_started', {
        'exercise_type': exercise_type,
        'message': f'Started {exercise_type} exercise'
    })

@socketio.on('video_frame')
def handle_video_frame(data):
    """Process video frame from WebRTC with optimized performance"""
    try:
        # Decode base64 image
        image_data = data.get('image')
        if not image_data:
            return
            
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64 to image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL to OpenCV format
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Resize frame to smaller size for faster processing
        frame = cv2.resize(frame, (640, 480))
        
        # Process frame based on exercise type
        session_id = request.sid
        if session_id in active_sessions:
            exercise_type = active_sessions[session_id]['exercise_type']
            result = process_exercise_frame(frame, exercise_type, session_id)
            
            # Send results back to client
            emit('exercise_feedback', result)
            
    except Exception as e:
        print(f"Error processing frame: {e}")
        emit('error', {'message': 'Error processing video frame'})

def process_exercise_frame(frame, exercise_type, session_id):
    """Process exercise frame and return feedback"""
    try:
        # Route to appropriate exercise processor
        if exercise_type == 'pushup':
            return process_pushup_frame(frame, session_id)
        elif exercise_type == 'left':
            return process_left_curl_frame(frame, session_id)
        elif exercise_type == 'right':
            return process_right_curl_frame(frame, session_id)
        elif exercise_type == 'squat':
            return process_squat_frame(frame, session_id)
        else:
            return {'error': 'Unknown exercise type'}
            
    except Exception as e:
        print(f"Error in process_exercise_frame: {e}")
        return {'error': str(e)}

if __name__ == '__main__':
    # Check if running in production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🏋️‍♀️ GymJam AI WebRTC Server Starting...")
    print(f"🌐 Server running on port {port}")
    print("📱 WebRTC enabled for cloud deployment")
    print("🎯 Features: Real-time pose detection, form feedback, progress tracking")
    print("🔗 Ready for Railway deployment!")
    
    socketio.run(app, host="0.0.0.0", port=port, debug=debug)
