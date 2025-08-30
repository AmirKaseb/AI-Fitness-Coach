# 🏋️‍♀️ GymJam AI Fitness Coach

A modern, AI-powered fitness application that uses MediaPipe for real-time pose detection and provides personalized exercise coaching with beautiful UI and motivational feedback.

## ✨ Features

### 🎯 **Exercise Tracking**
- **Real-time Count Display**: See your progress as you exercise
- **Target Goals**: Set and achieve specific rep targets for each exercise
- **Form Validation**: AI-powered feedback on your exercise form
- **Progress Visualization**: Beautiful progress bars and statistics

### 💪 **Supported Exercises**
- **Left Arm Curl** - Build strong biceps with proper form
- **Right Arm Curl** - Balanced arm development
- **Push-ups** - Full body strength training
- **Squats** - Leg power and endurance building

### 🎨 **Beautiful UI/UX**
- **Modern Design**: Gradient backgrounds and smooth animations
- **Responsive Layout**: Works perfectly on all screen sizes
- **Interactive Cards**: Click to select exercises with visual feedback
- **Real-time Updates**: Live exercise data and progress tracking

### 🧠 **AI Coaching Features**
- **Form Feedback**: Real-time corrections and encouragement
- **Motivational Messages**: Inspiring quotes that rotate automatically
- **Progress Statistics**: Track total exercises, perfect form, and calories burned
- **Pro Tips**: Expert advice for each exercise type

### 📱 **User Experience**
- **Count Display**: Clear rep counting with animations
- **Target Setting**: Customizable goals for each workout
- **Feedback System**: Color-coded messages (green for correct, red for corrections)
- **Demo Mode**: Animated demonstrations when camera isn't available

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Webcam or camera device
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/GymJam-AI-assistant-using-mediapipe.git
   cd GymJam-AI-assistant-using-mediapipe
   ```

2. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   python app.py
   ```

4. **Open the frontend**
   - Navigate to `frontend/index.html` in your browser
   - Or serve the frontend folder using a local server

## 🎮 How to Use

### 1. **Select Your Exercise**
- Choose from the four available exercises in the left panel
- Each exercise card shows the target reps and description

### 2. **Position Yourself**
- Stand in front of your camera
- Ensure good lighting for accurate pose detection
- Follow the on-screen instructions

### 3. **Start Exercising**
- The AI will detect your movements in real-time
- Watch the count increase as you complete reps
- Follow the feedback messages for proper form

### 4. **Track Progress**
- Monitor your count vs. target on screen
- View calories burned and form accuracy
- Get motivational feedback throughout your workout

## 🏗️ Architecture

### Frontend (`frontend/`)
- **HTML5**: Modern semantic structure
- **CSS3**: Beautiful gradients, animations, and responsive design
- **JavaScript**: Interactive functionality and real-time updates

### Backend (`backend/`)
- **Flask**: Python web framework
- **MediaPipe**: Google's pose detection library
- **OpenCV**: Computer vision processing
- **Real-time Video**: Live camera feed processing

### Key Files
- `frontend/index.html` - Main application interface
- `frontend/styles.css` - Beautiful styling and animations
- `frontend/script.js` - Interactive functionality
- `backend/app.py` - Main Flask application
- `backend/pose_*.py` - Exercise-specific pose detection
- `backend/PoseModule.py` - MediaPipe pose detection module

## 🎨 UI Components

### **Header Section**
- GymJam logo and branding
- User welcome message
- Professional gradient design

### **Left Panel - Exercise Selection**
- Interactive exercise cards
- Hover effects and animations
- Clear exercise descriptions

### **Center Panel - Video Feed**
- Real-time camera display
- Exercise count and target
- Form feedback messages
- Progress visualization

### **Right Panel - Motivation & Progress**
- Rotating motivational quotes
- Progress statistics
- Pro tips and advice
- Calorie tracking

## 🔧 Configuration

### Exercise Targets
Modify target reps in the JavaScript file:
```javascript
getExerciseTarget(exerciseType) {
    const targets = {
        'left': 12,    // Left arm curl target
        'right': 12,   // Right arm curl target
        'pushup': 10,  // Push-up target
        'squat': 15    // Squat target
    };
    return targets[exerciseType] || 10;
}
```

### Camera Settings
Adjust camera parameters in pose files:
```python
cap = cv2.VideoCapture(0)  # Change 0 to 1, 2, etc. for different cameras
```

## 🌟 Demo Mode

When the camera isn't available, the app automatically switches to demo mode:
- **Animated Stick Figures**: Visual exercise demonstrations
- **Progress Simulation**: Simulated count and feedback
- **Professional Appearance**: Maintains app functionality

## 📱 Responsive Design

The app is fully responsive and works on:
- **Desktop**: Full 3-panel layout
- **Tablet**: Adaptive grid layout
- **Mobile**: Single-column mobile-optimized view

## 🎯 Exercise Form Guidelines

### **Arm Curls**
- Keep your back straight
- Control the movement up and down
- Feel the burn in your biceps
- Maintain shoulder position

### **Push-ups**
- Keep your body in a straight line
- Lower your chest to the ground
- Push up with control
- Engage your core muscles

### **Squats**
- Keep your back straight
- Go as low as you can comfortably
- Push through your heels
- Keep your knees aligned with toes

## 🚀 Future Enhancements

- [ ] **User Accounts**: Personal progress tracking
- [ ] **Workout Plans**: Custom exercise routines
- [ ] **Social Features**: Share achievements with friends
- [ ] **Advanced Analytics**: Detailed performance metrics
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Voice Commands**: Hands-free exercise control

## 🤝 Contributing

We welcome contributions! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MediaPipe**: Google's pose detection technology
- **OpenCV**: Computer vision library
- **Flask**: Python web framework
- **Font Awesome**: Beautiful icons
- **Google Fonts**: Typography

## 📞 Support

If you need help or have questions:
- Create an issue on GitHub
- Check the documentation
- Review the code examples

---

**🏋️‍♀️ Get fit with AI! Start your fitness journey today with GymJam AI Fitness Coach! 💪**
