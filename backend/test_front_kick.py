"""
Test script for Front Kick Exercise
"""

import cv2
import numpy as np
import PoseModule as pm
from exercises.front_kick_webrtc import process_front_kick_frame

def test_front_kick():
    """Test the front kick exercise with webcam or video file"""
    
    # Initialize video capture (use 0 for webcam or path to video file)
    cap = cv2.VideoCapture(r"C:\Users\moustafa\Downloads\Muay Thai Front Kick_ instructional video.mp4")  # Change to video file path if needed
    
    # Create a mock session for testing
    session_id = "test_session"
    
    # Mock active_sessions for testing
    import sys
    sys.modules['app'] = type('MockApp', (), {
        'active_sessions': {
            session_id: {
                'count': 0,
                'calories': 0,
                'kick_counted': False
            }
        }
    })()
    
    print("Front Kick Exercise Test")
    print("Press 'q' to quit, 'r' to reset count")
    print("Requirements:")
    print("- Hip angle: 40°-70°")
    print("- Knee angle: 160°-180°")
    print("- Thigh parallel to floor")
    print("- Both angles must be in range to count rep")
    
    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to read frame")
            break
        
        # Resize frame for processing
        frame = cv2.resize(frame, (1280, 720))
        
        # Process the frame
        result = process_front_kick_frame(frame, session_id)
        
        # Display the processed frame
        cv2.imshow("Front Kick Exercise Test", frame)
        
        # Print results to console
        print(f"\rCount: {result['count']}, Calories: {result['calories']}, Form Score: {result['form_score']}, Feedback: {result['feedback']}", end="")
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            # Reset the session
            if hasattr(sys.modules['app'], 'active_sessions'):
                sys.modules['app'].active_sessions[session_id] = {
                    'count': 0,
                    'calories': 0,
                    'kick_counted': False
                }
            print("\nSession reset!")
    
    cap.release()
    cv2.destroyAllWindows()
    print("\nTest completed!")

if __name__ == "__main__":
    test_front_kick()

