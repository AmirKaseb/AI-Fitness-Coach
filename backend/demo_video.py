import cv2
import numpy as np
import math

def create_demo_video(exercise_type):
    """Create a demo video for the specified exercise type"""
    
    def generate_frame(frame_count, exercise_type):
        # Create a black canvas
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add gradient background
        for y in range(480):
            for x in range(640):
                img[y, x] = [
                    int(50 + (y / 480) * 100),  # Blue
                    int(30 + (x / 640) * 80),   # Green
                    int(100 + (y / 480) * 120)  # Red
                ]
        
        # Add exercise-specific animation
        if exercise_type == 'left' or exercise_type == 'right':
            draw_curl_demo(img, frame_count, exercise_type)
        elif exercise_type == 'pushup':
            draw_pushup_demo(img, frame_count)
        elif exercise_type == 'squat':
            draw_squat_demo(img, frame_count)
        
        # Add UI elements
        add_ui_elements(img, exercise_type, frame_count)
        
        return img
    
    def draw_curl_demo(img, frame_count, exercise_type):
        # Draw stick figure for curl
        center_x = 320
        center_y = 240
        
        # Head
        cv2.circle(img, (center_x, center_y - 80), 20, (255, 255, 255), -1)
        
        # Body
        cv2.line(img, (center_x, center_y - 60), (center_x, center_y + 40), (255, 255, 255), 3)
        
        # Arms
        arm_angle = math.sin(frame_count * 0.1) * 0.5 + 0.5  # 0 to 1
        if exercise_type == 'left':
            # Left arm curl
            arm_x = center_x - 40
            arm_y = center_y - 40
            elbow_x = arm_x + int(30 * arm_angle)
            elbow_y = arm_y + int(20 * arm_angle)
            wrist_x = elbow_x + int(25 * arm_angle)
            wrist_y = elbow_y + int(15 * arm_angle)
        else:
            # Right arm curl
            arm_x = center_x + 40
            arm_y = center_y - 40
            elbow_x = arm_x - int(30 * arm_angle)
            elbow_y = arm_y + int(20 * arm_angle)
            wrist_x = elbow_x - int(25 * arm_angle)
            wrist_y = elbow_y + int(15 * arm_angle)
        
        # Draw arm segments
        cv2.line(img, (center_x, center_y - 40), (arm_x, arm_y), (255, 255, 255), 3)
        cv2.line(img, (arm_x, arm_y), (elbow_x, elbow_y), (255, 255, 255), 3)
        cv2.line(img, (elbow_x, elbow_y), (wrist_x, wrist_y), (255, 255, 255), 3)
        
        # Legs
        cv2.line(img, (center_x, center_y + 40), (center_x - 20, center_y + 100), (255, 255, 255), 3)
        cv2.line(img, (center_x, center_y + 40), (center_x + 20, center_y + 100), (255, 255, 255), 3)
        
        # Add dumbbell
        if exercise_type == 'left':
            cv2.circle(img, (wrist_x, wrist_y), 15, (255, 215, 0), -1)  # Gold dumbbell
        else:
            cv2.circle(img, (wrist_x, wrist_y), 15, (255, 215, 0), -1)  # Gold dumbbell
    
    def draw_pushup_demo(img, frame_count):
        # Draw stick figure for pushup
        center_x = 320
        center_y = 240
        
        # Head
        cv2.circle(img, (center_x, center_y - 60), 15, (255, 255, 255), -1)
        
        # Body position based on frame
        body_angle = math.sin(frame_count * 0.15) * 0.3 + 0.7  # 0.4 to 1.0
        
        # Body
        body_end_x = center_x
        body_end_y = center_y + int(80 * body_angle)
        cv2.line(img, (center_x, center_y - 45), (body_end_x, body_end_y), (255, 255, 255), 3)
        
        # Arms
        arm_angle = math.sin(frame_count * 0.15) * 0.4 + 0.6  # 0.2 to 1.0
        left_arm_x = center_x - 30
        right_arm_x = center_x + 30
        arm_y = center_y - 30
        
        cv2.line(img, (center_x, center_y - 45), (left_arm_x, arm_y), (255, 255, 255), 3)
        cv2.line(img, (center_x, center_y - 45), (right_arm_x, arm_y), (255, 255, 255), 3)
        
        # Legs
        leg_angle = math.sin(frame_count * 0.15) * 0.3 + 0.7
        left_leg_x = center_x - 25
        right_leg_x = center_x + 25
        leg_y = center_y + int(60 * leg_angle)
        
        cv2.line(img, (body_end_x, body_end_y), (left_leg_x, leg_y), (255, 255, 255), 3)
        cv2.line(img, (body_end_x, body_end_y), (right_leg_x, leg_y), (255, 255, 255), 3)
    
    def draw_squat_demo(img, frame_count):
        # Draw stick figure for squat
        center_x = 320
        center_y = 240
        
        # Head
        cv2.circle(img, (center_x, center_y - 60), 15, (255, 255, 255), -1)
        
        # Body
        body_angle = math.sin(frame_count * 0.1) * 0.3 + 0.7  # 0.4 to 1.0
        body_end_x = center_x
        body_end_y = center_y + int(60 * body_angle)
        cv2.line(img, (center_x, center_y - 45), (body_end_x, body_end_y), (255, 255, 255), 3)
        
        # Arms (extended forward for balance)
        arm_angle = math.sin(frame_count * 0.1) * 0.2 + 0.8  # 0.6 to 1.0
        left_arm_x = center_x - int(40 * arm_angle)
        right_arm_x = center_x + int(40 * arm_angle)
        arm_y = center_y - 20
        
        cv2.line(img, (center_x, center_y - 45), (left_arm_x, arm_y), (255, 255, 255), 3)
        cv2.line(img, (center_x, center_y - 45), (right_arm_x, arm_y), (255, 255, 255), 3)
        
        # Legs (squat position)
        leg_angle = math.sin(frame_count * 0.1) * 0.4 + 0.6  # 0.2 to 1.0
        left_leg_x = center_x - 20
        right_leg_x = center_x + 20
        leg_y = center_y + int(80 * leg_angle)
        
        cv2.line(img, (body_end_x, body_end_y), (left_leg_x, leg_y), (255, 255, 255), 3)
        cv2.line(img, (body_end_x, body_end_y), (right_leg_x, leg_y), (255, 255, 255), 3)
    
    def add_ui_elements(img, exercise_type, frame_count):
        # Exercise title
        titles = {
            'left': 'Left Arm Curl Demo',
            'right': 'Right Arm Curl Demo',
            'pushup': 'Push-up Demo',
            'squat': 'Squat Demo'
        }
        title = titles.get(exercise_type, 'Exercise Demo')
        cv2.putText(img, title, (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Progress bar
        progress = (frame_count % 100) / 100.0
        bar_width = int(400 * progress)
        cv2.rectangle(img, (120, 70), (520, 85), (100, 100, 100), -1)
        cv2.rectangle(img, (120, 70), (120 + bar_width, 85), (0, 255, 0), -1)
        
        # Percentage
        cv2.putText(img, f'{int(progress * 100)}%', (530, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Demo indicator
        cv2.putText(img, 'DEMO MODE', (50, 420), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Instructions
        instructions = [
            "This is a demonstration video",
            "Position yourself in front of camera",
            "Follow the form shown above",
            "Keep proper posture throughout"
        ]
        
        for i, instruction in enumerate(instructions):
            y_pos = 450 + i * 20
            cv2.putText(img, instruction, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Generate frames
    frame_count = 0
    while True:
        frame = generate_frame(frame_count, exercise_type)
        
        # Encode frame
        ok, jpeg = cv2.imencode('.jpg', frame)
        if not ok:
            continue
            
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        
        frame_count += 1
        
        # Add small delay to control frame rate
        cv2.waitKey(50)

# Example usage:
# demo_video_feed = create_demo_video('left')
# for frame in demo_video_feed:
#     # Process frame
#     pass
