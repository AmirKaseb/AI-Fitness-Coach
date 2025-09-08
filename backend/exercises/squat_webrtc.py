"""
GymJam AI - Squat Exercise (WebRTC Version)
Clean, production-ready WebRTC implementation
"""

import cv2
import numpy as np
import PoseModule as pm
import base64
import io
from PIL import Image


def process_squat_frame(frame, session_id):
    """Process a single frame for squat detection and return feedback"""
    # Import active_sessions from app module
    import sys
    if 'app' in sys.modules:
        from app import active_sessions
    else:
        # Fallback for testing
        active_sessions = {}
    
    detector = pm.poseDetector()
    
    # Keep frame at smaller size for faster processing (already resized in app.py)
    frame = detector.findPose(frame, False)
    lmList = detector.findPosition(frame, False)
    
    result = {
        'count': 0,
        'calories': 0,
        'form_score': 0,
        'feedback': 'Stand straight with feet shoulder-width apart',
        'feedback_type': 'info',
        'form_good': False,
        'processed_frame': None
    }
    
    if len(lmList) != 0:
        # Calculate angles for squat form
        left_knee = detector.findAngle(frame, 23, 25, 27)
        right_knee = detector.findAngle(frame, 24, 26, 28)
        left_hip = detector.findAngle(frame, 11, 23, 25)
        right_hip = detector.findAngle(frame, 12, 24, 26)
        
        # Use average of both knees for squat detection
        knee_angle = (left_knee + right_knee) / 2
        hip_angle = (left_hip + right_hip) / 2
        
        # Calculate percentage of squat
        per = np.interp(knee_angle, (50, 160), (0, 100))
        bar = np.interp(knee_angle, (50, 160), (650, 100))
        
        # Check form
        if knee_angle > 160 and hip_angle > 160:
            form = 1
            result['feedback'] = "Great form! Ready to start"
            result['feedback_type'] = "correct"
            result['form_good'] = True
        else:
            form = 0
            result['feedback'] = "Get into proper starting position"
            result['feedback_type'] = "info"
            result['form_good'] = False
        
        # Check the direction and count squats
        if form == 1:
            if per == 0:
                if knee_angle <= 50 and hip_angle < 100:
                    result['feedback'] = "Down - Great form!"
                    result['feedback_type'] = "correct"
                    # Update session data
                    if session_id in active_sessions:
                        active_sessions[session_id]['count'] += 0.5
                        active_sessions[session_id]['calories'] += 5
                else:
                    result['feedback'] = "Fix Form - Go deeper"
                    result['feedback_type'] = "incorrect"
            
            if per == 100:
                if knee_angle > 160 and hip_angle > 160:
                    result['feedback'] = "Up - Perfect!"
                    result['feedback_type'] = "correct"
                    # Update session data
                    if session_id in active_sessions:
                        active_sessions[session_id]['count'] += 0.5
                        active_sessions[session_id]['calories'] += 5
                else:
                    result['feedback'] = "Fix Form - Stand up straight"
                    result['feedback_type'] = "incorrect"
        
        # Draw progress bar
        cv2.rectangle(frame, (1100, 100), (1175, 650), (0, 0, 0), 3)
        cv2.rectangle(frame, (1100, int(bar)), (1175, 650), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, f'{int(per)}%', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        
        # Draw squat counter
        cv2.rectangle(frame, (0, 0), (220, 185), (0, 0, 255), cv2.FILLED)
        current_count = active_sessions.get(session_id, {}).get('count', 0)
        cv2.putText(frame, str(int(current_count)), (70, 120), cv2.FONT_HERSHEY_PLAIN, 7, (255, 255, 255), 6)
        cv2.putText(frame, 'Squats', (10, 160), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        
        # Calories display
        current_calories = active_sessions.get(session_id, {}).get('calories', 0)
        cv2.putText(frame, f'Calories: {current_calories}', (10, 200), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        
        # Feedback display with color coding
        feedback_color = (0, 255, 0) if result['feedback_type'] == "correct" else (0, 0, 255) if result['feedback_type'] == "incorrect" else (255, 255, 0)
        cv2.putText(frame, result['feedback'], (50, 40), cv2.FONT_HERSHEY_PLAIN, 2, feedback_color, 2)
        
        # Form indicator
        if form == 1:
            cv2.putText(frame, "FORM: GOOD", (1000, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "FORM: ADJUSTING", (1000, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        
        # Target completion indicator
        if current_count >= 15:
            cv2.putText(frame, "SQUAT SET COMPLETED!", (400, 360), 
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            cv2.putText(frame, "Excellent leg workout!", (350, 410), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        
        # Convert processed frame back to base64 for sending to client (lower quality for speed)
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        result['processed_frame'] = f"data:image/jpeg;base64,{frame_base64}"
        
        # Update result with current session data
        if session_id in active_sessions:
            result['count'] = int(active_sessions[session_id]['count'])
            result['calories'] = active_sessions[session_id]['calories']
            result['form_score'] = int((knee_angle / 180) * 100)  # Simple form score based on knee angle
        
    else:
        result['feedback'] = "No person detected - please step in front of camera"
        result['feedback_type'] = "info"
        cv2.putText(frame, result['feedback'], (50, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
        
        # Convert frame to base64 even if no person detected
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        result['processed_frame'] = f"data:image/jpeg;base64,{frame_base64}"
    
    return result
