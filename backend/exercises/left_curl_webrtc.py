"""
GymJam AI - Left Arm Curl Exercise (WebRTC Version)
Clean, production-ready WebRTC implementation
"""

import cv2
import numpy as np
import PoseModule as pm
import base64
import io
from PIL import Image
from draw_arrow import up_arrow, down_arrow, colorful_up_arrow, colorful_down_arrow


def process_left_curl_frame(frame, session_id):
    """Process a single frame for left arm curl detection and return feedback"""
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
        'feedback': 'Position yourself in front of the camera',
        'feedback_type': 'info',
        'form_good': False,
        'processed_frame': None
    }
    
    if len(lmList) != 0:
        # Calculate angles for left arm curl
        elbow = detector.findAngle(frame, 11, 13, 15)
        shoulder = detector.findAngle(frame, 13, 11, 23)
        
        # Calculate percentage of curl
        per = np.interp(elbow, (50, 160), (0, 100))
        bar = np.interp(elbow, (50, 160), (650, 100))
        
        # Check form
        if elbow > 160 and shoulder > 40:
            form = 1
            result['feedback'] = "Great form! Ready to start"
            result['feedback_type'] = "correct"
            result['form_good'] = True
        else:
            form = 0
            result['feedback'] = "Get into proper starting position"
            result['feedback_type'] = "info"
            result['form_good'] = False
        
        # Check the direction and count curls
        if form == 1:
            if per == 0:
                if elbow <= 50:
                    result['feedback'] = "Up - Great form!"
                    result['feedback_type'] = "correct"
                    # Update session data
                    if session_id in active_sessions:
                        active_sessions[session_id]['count'] += 0.5
                        active_sessions[session_id]['calories'] += 3
                else:
                    result['feedback'] = "Fix Form - Keep arm straight"
                    result['feedback_type'] = "incorrect"
            
            if per == 100:
                if elbow > 160 and shoulder > 40:
                    result['feedback'] = "Down - Perfect!"
                    result['feedback_type'] = "correct"
                    # Update session data
                    if session_id in active_sessions:
                        active_sessions[session_id]['count'] += 0.5
                        active_sessions[session_id]['calories'] += 3
                else:
                    result['feedback'] = "Fix Form - Maintain position"
                    result['feedback_type'] = "incorrect"
        
        # Draw visual elements with arrows (same style as AI_trainer.py)
        up_arrow(img=frame)
        colorful_up_arrow(img=frame, percentage=per)
        cv2.putText(frame, f'{int(per)} %', (120, 430), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
        cv2.putText(frame, 'UP', (70, 600), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)

        down_arrow(img=frame)
        colorful_down_arrow(img=frame, percentage=100-per)
        cv2.putText(frame, 'DOWN', (1100, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
        cv2.putText(frame, f'{int(100-per)} %', (1050, 430), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)

        # Error graph (similar to AI_trainer.py)
        cv2.line(frame, (450, 100), (1000, 100), (0, 0, 255), 2)

        error_elbow_angle = int((elbow - 105) * 1.5)  # 105 is middle of 50-160 range
        error_shoulder_angle = int((shoulder - 40) * 1.5)

        cv2.circle(frame, (450, 100), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (450, 100), 7, (255, 0, 255), 2)

        cv2.circle(frame, (550, 100+error_elbow_angle), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (550, 100+error_elbow_angle), 7, (255, 0, 255), 2)

        cv2.line(frame, (450, 100), (550, 100+error_elbow_angle), (0, 255, 0), 2)

        cv2.line(frame, (550, 100+error_elbow_angle), (750, 100-error_shoulder_angle), (0, 255, 0), 2)

        cv2.circle(frame, (750, 100-error_shoulder_angle), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (750, 100-error_shoulder_angle), 7, (255, 0, 255), 2)

        cv2.circle(frame, (1000, 100), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (1000, 100), 7, (255, 0, 255), 2)

        cv2.line(frame, (750, 100-error_shoulder_angle), (1000, 100), (0, 255, 0), 2)

        # Show the error
        cv2.rectangle(frame, (220, 190), (510, 240), (100, 0, 0), 1)
        cv2.putText(frame, 'Elbow angle error:     %', (240, 210), cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 100, 0), 2)
        cv2.putText(frame, f'{round(abs(elbow - 105) / 55 * 100)}', (440, 210), cv2.FONT_HERSHEY_PLAIN, 1.1,
                    (0, 100, 0), 2)
        cv2.putText(frame, 'Shoulder angle error:     %', (240, 230), cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 100, 0), 2)
        cv2.putText(frame, f'{abs(round((shoulder - 40) / 20 * 100))}', (440, 230), cv2.FONT_HERSHEY_PLAIN, 1,
                    (0, 100, 0), 2)

        # Draw Left Curl Counter (same style as AI_trainer.py)
        cv2.rectangle(frame, (0, 0), (220, 185), (0, 100, 0), cv2.FILLED)
        current_count = active_sessions.get(session_id, {}).get('count', 0)
        cv2.putText(frame, str(int(current_count)), (70, 120), cv2.FONT_HERSHEY_PLAIN, 7, (255, 255, 255), 6)
        cv2.putText(frame, 'Left Curl', (10, 160), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        
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
        if current_count >= 12:
            cv2.putText(frame, "LEFT CURL SET COMPLETED!", (400, 360), 
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            cv2.putText(frame, "Great work on your left arm!", (350, 410), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        
        # Convert processed frame back to base64 for sending to client (lower quality for speed)
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        result['processed_frame'] = f"data:image/jpeg;base64,{frame_base64}"
        
        # Update result with current session data
        if session_id in active_sessions:
            result['count'] = int(active_sessions[session_id]['count'])
            result['calories'] = active_sessions[session_id]['calories']
            result['form_score'] = int((elbow / 180) * 100)  # Simple form score based on elbow angle
        
    else:
        result['feedback'] = "No person detected - please step in front of camera"
        result['feedback_type'] = "info"
        cv2.putText(frame, result['feedback'], (50, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
        
        # Convert frame to base64 even if no person detected
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        result['processed_frame'] = f"data:image/jpeg;base64,{frame_base64}"
    
    return result
