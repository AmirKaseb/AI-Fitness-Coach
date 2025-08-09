import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm

def right_curl():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "LOWER YOUR ARM"

    try:
        with detector.pose:
            while True:
                ret, img = cap.read()
                if not ret or img is None:
                    break

                img = detector.findPose(img, False)
                lmList = detector.findPosition(img, False)

                if len(lmList) != 0:
                    elbow = detector.findAngle(img, 12, 14, 16)
                    shoulder = detector.findAngle(img, 14, 12, 24)

                    per = np.interp(elbow, (40, 160), (100, 0))
                    bar = np.interp(elbow, (40, 160), (50, 380))

                    if shoulder < 40:
                        form = 1

                    if form == 1:
                        if per == 0:
                            if elbow > 160 and shoulder < 40:
                                feedback = "UP"
                                if direction == 0:
                                    count += 0.5
                                    direction = 1
                            else:
                                feedback = "LOWER YOUR ARM"

                        if per == 100:
                            if elbow < 40 and shoulder < 40:
                                feedback = "DOWN"
                                if direction == 1:
                                    count += 0.5
                                    direction = 0
                            else:
                                feedback = "LOWER YOUR ARM"
                else:
                    feedback = "NO PERSON DETECTED"

                h, w = img.shape[:2]
                bar_x1, bar_x2 = max(w - 60, 0), max(w - 40, 20)
                bar_bottom = min(380, h - 10)
                bar_top = int(np.clip(bar, 0, bar_bottom)) if 'bar' in locals() else 50

                if form == 1:
                    cv2.rectangle(img, (bar_x1, 50), (bar_x2, bar_bottom), (0, 255, 0), 3)
                    cv2.rectangle(img, (bar_x1, bar_top), (bar_x2, bar_bottom), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(per)}%', (max(w - 200, 10), min(230, h - 30)),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                counter_top = max(h - 100, 0)
                cv2.rectangle(img, (0, counter_top), (100, h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, min(h - 25, counter_top + 75)),
                            cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

                cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                ok, jpeg = cv2.imencode('.jpg', img)
                if not ok:
                    continue
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    finally:
        cap.release()
        cv2.destroyAllWindows()