import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm

def left_curl():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "Position yourself in front of the camera"
    feedback_type = "info"
    target = 12
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
                    elbow = detector.findAngle(img, 11, 13, 15)
                    shoulder = detector.findAngle(img, 13, 11, 23)

                    per = np.interp(elbow, (40, 160), (100, 0))
                    bar = np.interp(elbow, (40, 160), (50, 380))

                    if shoulder < 40:
                        form = 1

                    if form == 1:
                        if per == 0:
                            if elbow > 160 and shoulder < 40:
                                feedback = "Great! Now lower your arm slowly"
                                feedback_type = "correct"
                                if direction == 0:
                                    count += 0.5
                                    direction = 1
                                    calories += 2
                            else:
                                feedback = "Keep your arm up and shoulder steady"
                                feedback_type = "incorrect"

                        if per == 100:
                            if elbow < 40 and shoulder < 40:
                                feedback = "Perfect! Now lift your arm up"
                                feedback_type = "correct"
                                if direction == 1:
                                    count += 0.5
                                    direction = 0
                                    calories += 2
                            else:
                                feedback = "Lower your arm more and keep form"
                                feedback_type = "incorrect"
                    else:
                        feedback = "Stand straight and position your arm"
                        feedback_type = "info"
                else:
                    feedback = "No person detected - please step in front of camera"
                    feedback_type = "info"

                h, w = img.shape[:2]
                
                # Progress bar variables (used in form == 1 section)
                per = np.interp(elbow, (40, 160), (100, 0)) if 'elbow' in locals() else 0

                if form == 1:
                    # Clean progress bar - RIGHT SIDE with proper margins
                    bar_x1 = w - 50  # 50px from right edge
                    bar_x2 = w - 30  # 30px from right edge
                    bar_y1 = 80      # 80px from top (below feedback)
                    bar_y2 = h - 100 # 100px from bottom
                    
                    cv2.rectangle(img, (bar_x1, bar_y1), (bar_x2, bar_y2), (100, 100, 100), 3)
                    bar_fill_height = int((per / 100) * (bar_y2 - bar_y1))
                    bar_fill_y = bar_y2 - bar_fill_height
                    cv2.rectangle(img, (bar_x1, bar_fill_y), (bar_x2, bar_y2), (0, 255, 0), cv2.FILLED)
                    
                    # Clean percentage display - ABOVE progress bar
                    percentage_text = f'{int(per)}%'
                    percentage_size = cv2.getTextSize(percentage_text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
                    percentage_x = bar_x1 - percentage_size[0] - 20  # 20px left of progress bar
                    percentage_y = bar_y1 - 20  # 20px above progress bar
                    
                    # Background with proper margins
                    cv2.rectangle(img, (percentage_x - 8, percentage_y - percentage_size[1] - 8), 
                                (percentage_x + percentage_size[0] + 8, percentage_y + 8), (0, 0, 0), -1)
                    cv2.rectangle(img, (percentage_x - 8, percentage_y - percentage_size[1] - 8), 
                                (percentage_x + percentage_size[0] + 8, percentage_y + 8), (255, 255, 0), 2)
                    cv2.putText(img, percentage_text, (percentage_x, percentage_y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)

                # Clean count display - BOTTOM LEFT with proper margins
                counter_width = 100
                counter_height = 80
                counter_x = 20
                counter_y = h - counter_height - 20
                
                cv2.rectangle(img, (counter_x, counter_y), (counter_x + counter_width, counter_y + counter_height), (0, 255, 0), cv2.FILLED)
                cv2.rectangle(img, (counter_x, counter_y), (counter_x + counter_width, counter_y + counter_height), (255, 255, 255), 2)
                
                # Count text - centered in counter box
                count_text = f'{int(count)}/{target}'
                count_size = cv2.getTextSize(count_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)[0]
                count_x_centered = counter_x + (counter_width - count_size[0]) // 2
                count_y_centered = counter_y + (counter_height + count_size[1]) // 2
                cv2.putText(img, count_text, (count_x_centered, count_y_centered), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)

                # Clean calories display - ABOVE count box with proper margins
                calories_text = f'Calories: {calories}'
                calories_size = cv2.getTextSize(calories_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                calories_x = counter_x
                calories_y = counter_y - 15  # 15px above count box
                
                # Background with proper margins
                cv2.rectangle(img, (calories_x - 5, calories_y - calories_size[1] - 5), 
                            (calories_x + calories_size[0] + 5, calories_y + 5), (0, 0, 0), -1)
                cv2.rectangle(img, (calories_x - 5, calories_y - calories_size[1] - 5), 
                            (calories_x + calories_size[0] + 5, calories_y + 5), (255, 255, 255), 1)
                cv2.putText(img, calories_text, (calories_x, calories_y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Clean feedback display - TOP LEFT with proper margins
                feedback_color = (0, 255, 0) if feedback_type == "correct" else (0, 0, 255) if feedback_type == "incorrect" else (255, 255, 0)
                
                # Smaller font and better positioning
                text_size = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                feedback_x = 20
                feedback_y = 35
                
                # Background with proper margins
                cv2.rectangle(img, (feedback_x - 10, feedback_y - text_size[1] - 10), 
                            (feedback_x + text_size[0] + 10, feedback_y + 10), (0, 0, 0), -1)
                cv2.rectangle(img, (feedback_x - 10, feedback_y - text_size[1] - 10), 
                            (feedback_x + text_size[0] + 10, feedback_y + 10), feedback_color, 2)
                cv2.putText(img, feedback, (feedback_x, feedback_y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, feedback_color, 2)

                # Clean form indicator - TOP RIGHT with proper margins
                if form == 1:
                    form_text = "FORM: GOOD"
                    form_color = (0, 255, 0)
                else:
                    form_text = "FORM: ADJUSTING"
                    form_color = (0, 255, 255)
                
                form_size = cv2.getTextSize(form_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                form_x = w - form_size[0] - 20
                form_y = 35
                
                # Background with proper margins
                cv2.rectangle(img, (form_x - 10, form_y - form_size[1] - 10), 
                            (form_x + form_size[0] + 10, form_y + 10), (0, 0, 0), -1)
                cv2.rectangle(img, (form_x - 10, form_y - form_size[1] - 10), 
                            (form_x + form_size[0] + 10, form_y + 10), form_color, 2)
                cv2.putText(img, form_text, (form_x, form_y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, form_color, 2)

                # Clean completion indicator - CENTER with proper margins
                if count >= target:
                    # Main completion message
                    completion_text = "EXERCISE COMPLETED!"
                    completion_size = cv2.getTextSize(completion_text, cv2.FONT_HERSHEY_SIMPLEX, 1.8, 3)[0]
                    completion_x = (w - completion_size[0]) // 2
                    completion_y = h // 2 - 20
                    
                    # Background with proper margins
                    cv2.rectangle(img, (completion_x - 15, completion_y - completion_size[1] - 15), 
                                (completion_x + completion_size[0] + 15, completion_y + 15), (0, 0, 0), -1)
                    cv2.rectangle(img, (completion_x - 15, completion_y - completion_size[1] - 15), 
                                (completion_x + completion_size[0] + 15, completion_y + 15), (0, 255, 0), 2)
                    cv2.putText(img, completion_text, (completion_x, completion_y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 0), 3)
                    
                    # Subtitle message
                    subtitle_text = "Great job! Keep it up!"
                    subtitle_size = cv2.getTextSize(subtitle_text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
                    subtitle_x = (w - subtitle_size[0]) // 2
                    subtitle_y = h // 2 + 40
                    
                    # Background with proper margins
                    cv2.rectangle(img, (subtitle_x - 10, subtitle_y - subtitle_size[1] - 10), 
                                (subtitle_x + subtitle_size[0] + 10, subtitle_y + 10), (0, 0, 0), -1)
                    cv2.rectangle(img, (subtitle_x - 10, subtitle_y - subtitle_size[1] - 10), 
                                (subtitle_x + subtitle_size[0] + 10, subtitle_y + 10), (255, 255, 255), 1)
                    cv2.putText(img, subtitle_text, (subtitle_x, subtitle_y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

                ok, jpeg = cv2.imencode('.jpg', img)
                if not ok:
                    continue
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    finally:
        cap.release()
        cv2.destroyAllWindows()