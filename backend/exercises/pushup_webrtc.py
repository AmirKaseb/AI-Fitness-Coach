"""
GymJam AI - Push-up Exercise (WebRTC Version)
Clean, production-ready WebRTC implementation
"""

import cv2
import numpy as np
import PoseModule as pm
from draw_arrow import up_arrow, down_arrow, colorful_up_arrow, colorful_down_arrow
import base64
import io
from PIL import Image


def process_pushup_frame(frame, session_id):
    """Process a single frame for pushup detection and return feedback"""
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
    lmList = detector.land_mark_list(frame, False)
    
    result = {
        'count': 0,
        'calories': 0,
        'form_score': 0,
        'feedback': 'Position yourself in plank position',
        'feedback_type': 'info',
        'form_good': False,
        'processed_frame': None
    }
    
    if len(lmList) != 0:
        # Find the angle of the Right Elbow
        Right_elbow = detector.findAngle(frame, 12, 14, 16, height=40, width=-30)
        
        # Find the angle of the Right Shoulder
        Right_Shoulder = detector.findAngle(frame, 14, 12, 24, height=40, width=-30, show_angle=False)
        
        # Body alignment
        Body_angle = detector.findAngle(frame, 12, 24, 26, height=50, width=80)
        
        # Angle of right knee
        Knee_angle = detector.findAngle(frame, 24, 26, 28, height=50, width=80, show_angle=True)
        
        # Body perfect straight line
        detector.StraightBodyLine(frame, 12, 28)
        
        per = np.interp(Right_elbow, (75, 160), (0, 100))
        
        # Check to ensure right form before starting the program
        if Right_elbow > 160 and Right_Shoulder > 40 and Body_angle > 160:
            form = 1
            result['feedback'] = "Great form! Ready to start"
            result['feedback_type'] = "correct"
            result['form_good'] = True
        else:
            form = 0
            result['feedback'] = "Get into proper plank position"
            result['feedback_type'] = "info"
            result['form_good'] = False
        
        # Check the direction and counts push up
        if form == 1:
            if per == 0:
                if Right_elbow <= 90 and Body_angle > 160:
                    result['feedback'] = "Up - Great form!"
                    result['feedback_type'] = "correct"
                    # Update session data
                    if session_id in active_sessions:
                        active_sessions[session_id]['count'] += 0.5
                        active_sessions[session_id]['calories'] += 4
                else:
                    result['feedback'] = "Fix Form - Keep body straight"
                    result['feedback_type'] = "incorrect"
            
            if per == 100:
                if Right_elbow > 160 and Right_Shoulder > 40 and Body_angle > 160:
                    result['feedback'] = "Down - Perfect!"
                    result['feedback_type'] = "correct"
                    # Update session data
                    if session_id in active_sessions:
                        active_sessions[session_id]['count'] += 0.5
                        active_sessions[session_id]['calories'] += 4
                else:
                    result['feedback'] = "Fix Form - Maintain alignment"
                    result['feedback_type'] = "incorrect"
        
        # Draw visual elements
        up_arrow(img=frame)
        colorful_up_arrow(img=frame, percentage=per)
        cv2.putText(frame, f'{int(per)} %', (120, 430), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
        cv2.putText(frame, 'UP', (70, 600), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)
        
        down_arrow(img=frame)
        colorful_down_arrow(img=frame, percentage=100-per)
        cv2.putText(frame, 'DOWN', (1100, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
        cv2.putText(frame, f'{int(100-per)} %', (1050, 430), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
        
        # Draw Push-Up Counter
        cv2.rectangle(frame, (0, 0), (220, 185), (0, 0, 255), cv2.FILLED)
        current_count = active_sessions.get(session_id, {}).get('count', 0)
        cv2.putText(frame, str(int(current_count)), (70, 120), cv2.FONT_HERSHEY_PLAIN, 7, (255, 255, 255), 6)
        cv2.putText(frame, 'Push up', (10, 160), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        
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
        if current_count >= 10:
            cv2.putText(frame, "PUSHUP SET COMPLETED!", (400, 360), 
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            cv2.putText(frame, "Incredible strength! You're amazing!", (350, 410), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        
        # Convert processed frame back to base64 for sending to client (lower quality for speed)
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        result['processed_frame'] = f"data:image/jpeg;base64,{frame_base64}"
        
        # Update result with current session data
        if session_id in active_sessions:
            result['count'] = int(active_sessions[session_id]['count'])
            result['calories'] = active_sessions[session_id]['calories']
            result['form_score'] = int((Body_angle / 180) * 100)  # Simple form score based on body angle
        
    else:
        result['feedback'] = "No person detected - please step in front of camera"
        result['feedback_type'] = "info"
        cv2.putText(frame, result['feedback'], (50, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
        
        # Convert frame to base64 even if no person detected
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        result['processed_frame'] = f"data:image/jpeg;base64,{frame_base64}"
    
    return result
