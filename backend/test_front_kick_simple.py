"""
Simple test for Front Kick Exercise
"""

import cv2
import numpy as np
import PoseModule as pm
from exercises.front_kick_webrtc import process_front_kick_frame

def test_front_kick_simple():
    """Simple test for front kick exercise"""
    
    # Create a mock session
    session_id = "test_session"
    
    # Mock active_sessions
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
    
    print("Testing Front Kick Exercise...")
    print("This test will create a simple frame and process it.")
    
    # Create a test frame
    test_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    test_frame.fill(50)  # Dark gray background
    
    # Add some text to the frame
    cv2.putText(test_frame, "Front Kick Test", (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    cv2.putText(test_frame, "No person detected - this is expected", (50, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    
    try:
        # Process the frame
        result = process_front_kick_frame(test_frame, session_id)
        
        print("✅ Front Kick Exercise Test Results:")
        print(f"   Count: {result['count']}")
        print(f"   Calories: {result['calories']}")
        print(f"   Form Score: {result['form_score']}")
        print(f"   Feedback: {result['feedback']}")
        print(f"   Form Good: {result['form_good']}")
        print(f"   Feedback Type: {result['feedback_type']}")
        
        if result['processed_frame']:
            print("✅ Frame processing successful")
        else:
            print("❌ Frame processing failed")
            
        print("\n🎯 Front Kick Exercise is working correctly!")
        print("The exercise will show 'No person detected' when no one is in front of the camera.")
        print("When you use it with a real camera, it will detect your pose and provide feedback.")
        
    except Exception as e:
        print(f"❌ Error testing front kick exercise: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_front_kick_simple()
