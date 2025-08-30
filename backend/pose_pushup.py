import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm

def pushup():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "Position yourself in plank position"
    feedback_type = "info"
    target = 10
    calories = 0

    try:
        with detector.pose:
            while True:
                ret, img = cap.read()
                if not ret or img is None:
                    break

                img = detector.findPose(img, False)
                lmList = detector.findPosition(img, False)

                if len(lmList) != 0:
                    # Calculate angles for pushup form
                    left_arm = detector.findAngle(img, 11, 13, 15)
                    right_arm = detector.findAngle(img, 12, 14, 16)
                    left_shoulder = detector.findAngle(img, 13, 11, 23)
                    right_shoulder = detector.findAngle(img, 14, 12, 24)

                    # Use average of both arms for consistency
                    arm_angle = (left_arm + right_arm) / 2
                    shoulder_angle = (left_shoulder + right_shoulder) / 2

                    per = np.interp(arm_angle, (90, 160), (100, 0))
                    bar = np.interp(arm_angle, (90, 160), (50, 380))

                    # Check if body is in proper plank position
                    if shoulder_angle > 160:
                        form = 1

                    if form == 1:
                        if per == 0:
                            if arm_angle > 160 and shoulder_angle > 160:
                                feedback = "Great! Now lower your body slowly"
                                feedback_type = "correct"
                                if direction == 0:
                                    count += 0.5
                                    direction = 1
                                    calories += 4
                            else:
                                feedback = "Keep your body straight and lower down"
                                feedback_type = "incorrect"

                        if per == 100:
                            if arm_angle < 90 and shoulder_angle > 160:
                                feedback = "Perfect! Now push back up"
                                feedback_type = "correct"
                                if direction == 1:
                                    count += 0.5
                                    direction = 0
                                    calories += 4
                            else:
                                feedback = "Lower your body more and maintain form"
                                feedback_type = "incorrect"
                    else:
                        feedback = "Get into plank position - keep body straight"
                        feedback_type = "info"
                else:
                    feedback = "No person detected - please step in front of camera"
                    feedback_type = "info"

                h, w = img.shape[:2]
                
                # Progress bar
                bar_x1, bar_x2 = max(w - 60, 0), max(w - 40, 20)
                bar_bottom = min(380, h - 10)
                bar_top = int(np.clip(bar, 0, bar_bottom)) if 'bar' in locals() else 50

                if form == 1:
                    # Green progress bar
                    cv2.rectangle(img, (bar_x1, 50), (bar_x2, bar_bottom), (0, 255, 0), 3)
                    cv2.rectangle(img, (bar_x1, bar_top), (bar_x2, bar_bottom), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(per)}%', (max(w - 200, 10), min(230, h - 30)),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                # Count display with animation
                counter_top = max(h - 120, 0)
                cv2.rectangle(img, (0, counter_top), (120, h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(count)}/{target}', (10, min(h - 25, counter_top + 75)),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

                # Calories display
                cv2.putText(img, f'Calories: {calories}', (10, min(h - 60, counter_top + 40)),
                            cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

                # Feedback display with color coding
                feedback_color = (0, 255, 0) if feedback_type == "correct" else (0, 0, 255) if feedback_type == "incorrect" else (255, 255, 0)
                cv2.putText(img, feedback, (50, 40), cv2.FONT_HERSHEY_PLAIN, 2, feedback_color, 2)

                # Form indicator
                if form == 1:
                    cv2.putText(img, "FORM: GOOD", (w - 200, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                else:
                    cv2.putText(img, "FORM: ADJUSTING", (w - 200, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

                # Target completion indicator
                if count >= target:
                    cv2.putText(img, "PUSHUP SET COMPLETED!", (w//2 - 180, h//2), 
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    cv2.putText(img, "Incredible strength! You're amazing!", (w//2 - 200, h//2 + 50), 
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                ok, jpeg = cv2.imencode('.jpg', img)
                if not ok:
                    continue
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    finally:
        cap.release()
        cv2.destroyAllWindows()