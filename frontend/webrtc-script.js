// WebRTC-enabled GymJam AI Assistant
// This script handles WebRTC video streaming and real-time pose detection

class WebRTCGymJam {
    constructor() {
        this.socket = null;
        this.video = null;
        this.canvas = null;
        this.ctx = null;
        this.stream = null;
        this.isStreaming = false;
        this.currentExercise = null;
        this.frameInterval = null;
        this.sessionId = null;
        
        this.init();
    }
    
    init() {
        this.setupSocketConnection();
        this.setupVideoElements();
        this.setupEventListeners();
    }
    
    setupSocketConnection() {
        // Connect to Flask-SocketIO server
        this.socket = io('http://localhost:5000');
        
        this.socket.on('connect', () => {
            console.log('Connected to GymJam AI server');
            this.sessionId = this.socket.id;
            this.showToast('success', 'Connected', 'Connected to AI server');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.showToast('warning', 'Disconnected', 'Lost connection to server');
        });
        
        this.socket.on('exercise_started', (data) => {
            console.log('Exercise started:', data);
            this.showToast('success', 'Exercise Started', data.message);
        });
        
        this.socket.on('exercise_feedback', (data) => {
            this.handleExerciseFeedback(data);
        });
        
        this.socket.on('error', (data) => {
            console.error('Server error:', data);
            this.showToast('error', 'Error', data.message);
        });
    }
    
    setupVideoElements() {
        // Create video element for camera access
        this.video = document.createElement('video');
        this.video.autoplay = true;
        this.video.playsInline = true;
        this.video.style.display = 'none';
        
        // Create canvas for frame capture
        this.canvas = document.createElement('canvas');
        this.canvas.width = 640;
        this.canvas.height = 480;
        this.ctx = this.canvas.getContext('2d');
        
        document.body.appendChild(this.video);
        document.body.appendChild(this.canvas);
    }
    
    setupEventListeners() {
        // Add event listeners for exercise buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('exercise-btn')) {
                const exerciseType = e.target.getAttribute('data-exercise');
                if (exerciseType) {
                    this.startExercise(exerciseType);
                }
            }
        });
    }
    
    async startCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                }
            });
            
            this.video.srcObject = this.stream;
            
            return new Promise((resolve) => {
                this.video.onloadedmetadata = () => {
                    resolve(true);
                };
            });
        } catch (error) {
            console.error('Error accessing camera:', error);
            this.showToast('error', 'Camera Error', 'Could not access camera. Please check permissions.');
            return false;
        }
    }
    
    async startExercise(exerciseType) {
        if (!this.socket || !this.socket.connected) {
            this.showToast('error', 'Connection Error', 'Not connected to server');
            return;
        }
        
        // Start camera if not already started
        if (!this.stream) {
            const cameraStarted = await this.startCamera();
            if (!cameraStarted) {
                return;
            }
        }
        
        this.currentExercise = exerciseType;
        
        // Notify server to start exercise
        this.socket.emit('start_exercise', {
            exercise_type: exerciseType
        });
        
        // Start frame streaming
        this.startFrameStreaming();
        
        // Show video container
        this.showVideoContainer();
    }
    
    startFrameStreaming() {
        if (this.frameInterval) {
            clearInterval(this.frameInterval);
        }
        
        this.isStreaming = true;
        this.frameCount = 0;
        
        // Send frames at 10 FPS (every 100ms) for better performance
        // Skip every other frame to reduce processing load
        this.frameInterval = setInterval(() => {
            if (this.isStreaming && this.video.videoWidth > 0) {
                this.frameCount++;
                // Only process every 2nd frame to reduce latency
                if (this.frameCount % 2 === 0) {
                    this.captureAndSendFrame();
                }
            }
        }, 100);
    }
    
    captureAndSendFrame() {
        // Draw current video frame to canvas
        this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
        
        // Convert canvas to base64 with lower quality for faster processing
        const imageData = this.canvas.toDataURL('image/jpeg', 0.6);
        
        // Send frame to server
        this.socket.emit('video_frame', {
            image: imageData,
            exercise_type: this.currentExercise
        });
    }
    
    handleExerciseFeedback(data) {
        // Update UI with feedback
        this.updateExerciseStats(data);
        this.updateFeedbackDisplay(data);
        
        // Update video display if processed frame is available
        if (data.processed_frame) {
            this.updateVideoDisplay(data.processed_frame);
        }
    }
    
    updateExerciseStats(data) {
        // Update rep count
        const repCountElement = document.getElementById('repCount');
        if (repCountElement) {
            repCountElement.textContent = data.count || 0;
        }
        
        // Update calorie count
        const calorieElement = document.getElementById('calorieCount');
        if (calorieElement) {
            calorieElement.textContent = data.calories || 0;
        }
        
        // Update form score
        const formScoreElement = document.getElementById('formScore');
        if (formScoreElement) {
            formScoreElement.textContent = `${data.form_score || 0}%`;
        }
    }
    
    updateFeedbackDisplay(data) {
        const feedbackElement = document.getElementById('feedbackText');
        if (feedbackElement) {
            feedbackElement.textContent = data.feedback || 'Ready to start your workout!';
            
            // Update feedback color based on type
            const feedbackContainer = document.getElementById('voiceFeedback');
            if (feedbackContainer) {
                feedbackContainer.className = 'feedback-message';
                if (data.feedback_type === 'correct') {
                    feedbackContainer.classList.add('correct');
                } else if (data.feedback_type === 'incorrect') {
                    feedbackContainer.classList.add('incorrect');
                } else {
                    feedbackContainer.classList.add('info');
                }
            }
        }
    }
    
    updateVideoDisplay(processedFrameData) {
        const videoElement = document.getElementById('videoStream');
        if (videoElement) {
            videoElement.src = processedFrameData;
        }
    }
    
    showVideoContainer() {
        const videoContainer = document.getElementById('videoContainer');
        if (videoContainer) {
            videoContainer.classList.remove('hidden');
        }
        
        // Switch to workout section
        this.showSection('workout');
    }
    
    stopExercise() {
        this.isStreaming = false;
        
        if (this.frameInterval) {
            clearInterval(this.frameInterval);
            this.frameInterval = null;
        }
        
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        this.currentExercise = null;
        
        // Hide video container
        const videoContainer = document.getElementById('videoContainer');
        if (videoContainer) {
            videoContainer.classList.add('hidden');
        }
        
        this.showToast('info', 'Exercise Stopped', 'Workout session ended');
    }
    
    showSection(sectionName) {
        // Hide all sections
        const sections = document.querySelectorAll('.app-section');
        sections.forEach(section => section.classList.add('hidden'));
        
        // Show target section
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.classList.remove('hidden');
        }
        
        // Update navigation
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => link.classList.remove('active'));
        
        const activeLink = document.querySelector(`[onclick="showSection('${sectionName}')"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }
    
    showToast(type, title, message) {
        // Simple toast notification
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <strong>${title}</strong><br>
                ${message}
            </div>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Global functions for HTML onclick handlers
let gymJamApp;

function startWorkoutFlow() {
    if (!gymJamApp) {
        gymJamApp = new WebRTCGymJam();
    }
    gymJamApp.showSection('workout');
}

function selectExercise(exerciseType) {
    if (gymJamApp) {
        gymJamApp.startExercise(exerciseType);
    }
}

function startWorkout() {
    // Workout is started when exercise is selected
    console.log('Workout started');
}

function stopWorkout() {
    if (gymJamApp) {
        gymJamApp.stopExercise();
    }
}

function resetWorkout() {
    if (gymJamApp) {
        gymJamApp.stopExercise();
        // Reset UI elements
        document.getElementById('repCount').textContent = '0';
        document.getElementById('calorieCount').textContent = '0';
        document.getElementById('formScore').textContent = '0%';
        document.getElementById('feedbackText').textContent = 'Ready to start your workout!';
    }
}

function closeVideo() {
    if (gymJamApp) {
        gymJamApp.stopExercise();
    }
}

function showSection(sectionName) {
    if (gymJamApp) {
        gymJamApp.showSection(sectionName);
    }
}

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', () => {
    gymJamApp = new WebRTCGymJam();
});

// Add CSS for toast notifications
const style = document.createElement('style');
style.textContent = `
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    }
    
    .toast.show {
        transform: translateX(0);
    }
    
    .toast.success {
        border-left: 4px solid #10b981;
    }
    
    .toast.error {
        border-left: 4px solid #ef4444;
    }
    
    .toast.warning {
        border-left: 4px solid #f59e0b;
    }
    
    .toast.info {
        border-left: 4px solid #3b82f6;
    }
    
    .feedback-message.correct {
        color: #10b981;
    }
    
    .feedback-message.incorrect {
        color: #ef4444;
    }
    
    .feedback-message.info {
        color: #f59e0b;
    }
`;
document.head.appendChild(style);
