"""
GymJam AI - Front Kick Exercise (WebRTC Version)
Clean, production-ready WebRTC implementation for front kick detection
"""

import cv2
import numpy as np
import PoseModule as pm
import base64
import io
from PIL import Image
from draw_arrow import up_arrow, down_arrow, colorful_up_arrow, colorful_down_arrow


def process_front_kick_frame(frame, session_id):
    """Process a single frame for front kick detection and return feedback"""
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
        'feedback': 'Stand ready for front kick',
        'feedback_type': 'info',
        'form_good': False,
        'processed_frame': None
    }
    
    if len(lmList) != 0:
        # Get landmarks for both legs
        # Left leg landmarks: hip (23), knee (25), ankle (27)
        # Right leg landmarks: hip (24), knee (26), ankle (28)
        
        # Calculate hip angles for both legs (hip-knee-ankle)
        left_hip_angle = detector.findAngle(frame, 23, 25, 27, height=40, width=-30, show_angle=True)
        right_hip_angle = detector.findAngle(frame, 24, 26, 28, height=40, width=-30, show_angle=True)
        
        # Calculate knee angles for both legs (hip-knee-foot)
        left_knee_angle = detector.findAngle(frame, 23, 25, 27, height=50, width=80, show_angle=True)
        right_knee_angle = detector.findAngle(frame, 24, 26, 28, height=50, width=80, show_angle=True)
        
        # Calculate thigh height (check if thigh is parallel to floor)
        # We'll use the hip and knee positions to determine thigh height
        left_thigh_height = abs(lmList[23][2] - lmList[25][2])  # y-coordinate difference
        right_thigh_height = abs(lmList[24][2] - lmList[26][2])  # y-coordinate difference
        
        # Determine which leg is kicking (higher thigh = kicking leg)
        kicking_leg = "left" if left_thigh_height > right_thigh_height else "right"
        
        # Get the angles for the kicking leg
        if kicking_leg == "left":
            hip_angle = left_hip_angle
            knee_angle = left_knee_angle
            thigh_height = left_thigh_height
        else:
            hip_angle = right_hip_angle
            knee_angle = right_knee_angle
            thigh_height = right_thigh_height
        
        # Calculate percentage for motion progress (similar to pushup logic)
        # Use hip angle to determine kick progress (40-70 degrees is the target range)
        # We'll map the hip angle to a percentage where 40° = 0% and 70° = 100%
        per = np.interp(hip_angle, (40, 70), (0, 100))
        per = max(0, min(100, per))  # Clamp between 0 and 100
        
        # Check if both hip and knee angles are in target range
        hip_in_range = 40 <= hip_angle <= 70
        knee_in_range = 160 <= knee_angle <= 180
        
        # Check if thigh is at least parallel to floor (simplified check)
        thigh_parallel = thigh_height > 50  # Adjust threshold based on testing
        
        # Determine if form is good
        form_good = hip_in_range and knee_in_range and thigh_parallel
        
        # Check to ensure right form before starting the program
        if hip_in_range and knee_in_range and thigh_parallel:
            form = 1
            result['feedback'] = "Great form! Ready to kick"
            result['feedback_type'] = "correct"
            result['form_good'] = True
        else:
            form = 0
            result['feedback'] = "Get into proper kicking position"
            result['feedback_type'] = "info"
            result['form_good'] = False
        
        # Check the direction and counts front kick
        if form == 1:
            # Count the rep when both angles are in range and motion is complete
            if per >= 80:  # When kick is at peak (80%+ of target range)
                if hip_in_range and knee_in_range:
                    result['feedback'] = "Perfect kick! Great form!"
                    result['feedback_type'] = "correct"
                    # Update session data
                    if session_id in active_sessions:
                        if not active_sessions[session_id].get('kick_counted', False):
                            active_sessions[session_id]['count'] += 1
                            active_sessions[session_id]['calories'] += 3
                            active_sessions[session_id]['kick_counted'] = True
                else:
                    result['feedback'] = "Fix Form - Keep proper angles"
                    result['feedback_type'] = "incorrect"
            elif per <= 20:  # When kick is at start
                if hip_in_range and knee_in_range:
                    result['feedback'] = "Ready to kick - Great form!"
                    result['feedback_type'] = "correct"
                    # Reset kick_counted when back to start position
                    if session_id in active_sessions:
                        active_sessions[session_id]['kick_counted'] = False
                else:
                    result['feedback'] = "Fix Form - Adjust your position"
                    result['feedback_type'] = "incorrect"
            else:
                result['feedback'] = "Kick in progress - Maintain form"
                result['feedback_type'] = "info"
        
        # Draw visual elements with arrows (same style as AI_trainer.py)
        up_arrow(img=frame)
        colorful_up_arrow(img=frame, percentage=per)
        cv2.putText(frame, f'{int(per)} %', (120, 430), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
        cv2.putText(frame, 'KICK UP', (70, 600), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)

        down_arrow(img=frame)
        colorful_down_arrow(img=frame, percentage=100-per)
        cv2.putText(frame, 'RETURN', (1100, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
        cv2.putText(frame, f'{int(100-per)} %', (1050, 430), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)

        # Error graph (similar to AI_trainer.py)
        cv2.line(frame, (450, 100), (1000, 100), (0, 0, 255), 2)

        error_hip_angle = int((hip_angle - 55) * 2)  # 55 is middle of 40-70 range
        error_knee_angle = int((knee_angle - 170) * 2)  # 170 is middle of 160-180 range

        cv2.circle(frame, (450, 100), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (450, 100), 7, (255, 0, 255), 2)

        cv2.circle(frame, (550, 100+error_hip_angle), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (550, 100+error_hip_angle), 7, (255, 0, 255), 2)

        cv2.line(frame, (450, 100), (550, 100+error_hip_angle), (0, 255, 0), 2)

        cv2.line(frame, (550, 100+error_hip_angle), (750, 100-error_knee_angle), (0, 255, 0), 2)

        cv2.circle(frame, (750, 100-error_knee_angle), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (750, 100-error_knee_angle), 7, (255, 0, 255), 2)

        cv2.circle(frame, (1000, 100), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (1000, 100), 7, (255, 0, 255), 2)

        cv2.line(frame, (750, 100-error_knee_angle), (1000, 100), (0, 255, 0), 2)

        # Show the error
        cv2.rectangle(frame, (220, 190), (510, 240), (100, 0, 0), 1)
        cv2.putText(frame, 'Hip angle error:     %', (240, 210), cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 100, 0), 2)
        cv2.putText(frame, f'{round(abs(hip_angle - 55) / 15 * 100)}', (440, 210), cv2.FONT_HERSHEY_PLAIN, 1.1,
                    (0, 100, 0), 2)
        cv2.putText(frame, 'Knee angle error:     %', (240, 230), cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 100, 0), 2)
        cv2.putText(frame, f'{abs(round((knee_angle - 170) / 10 * 100))}', (440, 230), cv2.FONT_HERSHEY_PLAIN, 1,
                    (0, 100, 0), 2)

        # Draw Front Kick Counter (same style as AI_trainer.py)
        cv2.rectangle(frame, (0, 0), (220, 185), (0, 100, 0), cv2.FILLED)
        current_count = active_sessions.get(session_id, {}).get('count', 0)
        cv2.putText(frame, str(int(current_count)), (70, 120), cv2.FONT_HERSHEY_PLAIN, 7, (255, 255, 255), 6)
        cv2.putText(frame, 'Front Kick', (10, 160), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        
        # Calories display
        current_calories = active_sessions.get(session_id, {}).get('calories', 0)
        cv2.putText(frame, f'Calories: {current_calories}', (10, 200), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        
        # Feedback display with color coding
        feedback_color = (0, 255, 0) if result['feedback_type'] == "correct" else (0, 0, 255) if result['feedback_type'] == "incorrect" else (255, 255, 0)
        cv2.putText(frame, result['feedback'], (50, 40), cv2.FONT_HERSHEY_PLAIN, 2, feedback_color, 2)
        
        # Form indicator
        if form_good:
            cv2.putText(frame, "FORM: EXCELLENT", (1000, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "FORM: ADJUSTING", (1000, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        
        # Target completion indicator
        if current_count >= 10:
            cv2.putText(frame, "FRONT KICK SET COMPLETED!", (400, 360), 
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            cv2.putText(frame, "Excellent kicking technique!", (350, 410), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        
        # Convert processed frame back to base64 for sending to client (lower quality for speed)
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        result['processed_frame'] = f"data:image/jpeg;base64,{frame_base64}"
        
        # Update result with current session data
        if session_id in active_sessions:
            result['count'] = int(active_sessions[session_id]['count'])
            result['calories'] = active_sessions[session_id]['calories']
            # Form score based on how close angles are to target ranges
            hip_score = max(0, 100 - abs(hip_angle - 55) * 2)  # 55 is middle of 40-70 range
            knee_score = max(0, 100 - abs(knee_angle - 170) * 2)  # 170 is middle of 160-180 range
            result['form_score'] = int((hip_score + knee_score) / 2)
        
    else:
        result['feedback'] = "No person detected - please step in front of camera"
        result['feedback_type'] = "info"
        cv2.putText(frame, result['feedback'], (50, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
        
        # Convert frame to base64 even if no person detected
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        result['processed_frame'] = f"data:image/jpeg;base64,{frame_base64}"
    
    return result
