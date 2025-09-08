#!/usr/bin/env python3
"""
Test script for WebRTC GymJam AI Assistant
This script tests the WebRTC functionality without requiring a full deployment
"""

import cv2
import numpy as np
import base64
import io
from PIL import Image
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_frame_processing():
    """Test the frame processing functionality"""
    print("🧪 Testing WebRTC Frame Processing...")
    
    try:
        # Import our modules
        from pose_pushup import process_pushup_frame
        
        # Create a test frame (640x480 black image)
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add some test content to make it more realistic
        cv2.putText(test_frame, "Test Frame", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
        print("✅ Test frame created")
        
        # Test the frame processing function
        result = process_pushup_frame(test_frame, "test_session")
        
        print("✅ Frame processing completed")
        print(f"📊 Result keys: {list(result.keys())}")
        print(f"📈 Count: {result.get('count', 'N/A')}")
        print(f"🔥 Calories: {result.get('calories', 'N/A')}")
        print(f"📝 Feedback: {result.get('feedback', 'N/A')}")
        print(f"🎯 Form Score: {result.get('form_score', 'N/A')}")
        
        if result.get('processed_frame'):
            print("✅ Processed frame generated successfully")
        else:
            print("⚠️  No processed frame in result")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing frame processing: {e}")
        return False

def test_base64_conversion():
    """Test base64 image conversion"""
    print("\n🧪 Testing Base64 Image Conversion...")
    
    try:
        # Create a test image
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.putText(test_image, "TEST", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', test_image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        print("✅ Image converted to base64")
        
        # Convert back from base64
        image_bytes = base64.b64decode(image_base64)
        pil_image = Image.open(io.BytesIO(image_bytes))
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        print("✅ Base64 converted back to OpenCV image")
        print(f"📐 Image shape: {opencv_image.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing base64 conversion: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available"""
    print("\n🧪 Testing Dependencies...")
    
    dependencies = [
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
        ('base64', 'Base64'),
        ('io', 'IO'),
    ]
    
    all_good = True
    
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {display_name} - Available")
        except ImportError:
            print(f"❌ {display_name} - Missing")
            all_good = False
    
    # Test our custom modules
    try:
        import PoseModule
        print("✅ PoseModule - Available")
    except ImportError:
        print("❌ PoseModule - Missing")
        all_good = False
    
    try:
        import draw_arrow
        print("✅ draw_arrow - Available")
    except ImportError:
        print("❌ draw_arrow - Missing")
        all_good = False
    
    return all_good

def main():
    """Run all tests"""
    print("🚀 GymJam AI WebRTC Test Suite")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Base64 Conversion", test_base64_conversion),
        ("Frame Processing", test_frame_processing),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} Test...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! WebRTC setup is ready.")
        print("\n🚀 Next steps:")
        print("1. Run: python app.py")
        print("2. Open: frontend/webrtc-demo.html")
        print("3. Test the WebRTC functionality")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
