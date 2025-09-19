from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from pose_left import left_curl
from pose_right import right_curl
from pose_pushup import pushup
from pose_squat import squat
from exercises.front_kick_webrtc import process_front_kick_frame
import cv2
import mediapipe as mp
import numpy as np
import os
import base64
import io
from PIL import Image
import PoseModule as pm
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def front_kick():
    """Front kick exercise generator"""

    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        img = cv2.resize(img, (1280, 720))
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        if len(lmList) != 0:
            # Process the frame using the WebRTC function
            result = process_front_kick_frame(img, "default_session")
            # The processed frame is already in the result, but we need to return it as a generator
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for demo mode
demo_mode = False
demo_exercise = None

# Global variables for WebRTC processing
current_exercise = None
active_sessions = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/webrtc')
def webrtc():
    """Serve the WebRTC interface"""
    return render_template('webrtc.html')

@app.route('/webrtc-demo')
def webrtc_demo():
    """Serve the WebRTC demo interface"""
    return render_template('webrtc_demo.html')

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

@app.route('/video_feed_frontkick')
def video_feed_frontkick():
    return Response(front_kick(),
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

# WebSocket event handlers for WebRTC
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to GymJam AI'})

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
        # Import the appropriate exercise module
        if exercise_type == 'pushup':
            from pose_pushup import process_pushup_frame
            return process_pushup_frame(frame, session_id)
        elif exercise_type == 'left':
            from exercises.left_curl_webrtc import process_left_curl_frame
            return process_left_curl_frame(frame, session_id)
        elif exercise_type == 'right':
            from exercises.right_curl_webrtc import process_right_curl_frame
            return process_right_curl_frame(frame, session_id)
        elif exercise_type == 'squat':
            from exercises.squat_webrtc import process_squat_frame
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
    
    print("🏋️‍♀️ GymJam AI Fitness Coach Starting...")
    print(f"🌐 Server running on port {port}")
    print("📱 Open your browser and navigate to the frontend")
    print("🎯 Features: Real-time pose detection, form feedback, progress tracking")
    print("🔗 WebRTC enabled for cloud deployment")
    
    socketio.run(app, host="0.0.0.0", port=port, debug=debug)