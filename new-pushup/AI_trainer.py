import cv2
import numpy as np
import PoseModule as pm
import time
from draw_arrow import up_arrow, down_arrow, colorful_up_arrow, colorful_down_arrow


codec = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter('push-up-detection.avi', codec, 20, (1280, 720))

cap = cv2.VideoCapture('push-up1.mp4')
detector = pm.poseDetector()
count = 0
direction = 0
form = 0

while True:
    success, img = cap.read()

    img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img, False)
    lmList = detector.land_mark_list(img, False)

    if len(lmList) != 0:
        # find the angle of the Right Elbow
        Right_elbow = detector.findAngle(img, 12, 14, 16, height=40, width=-30)

        # find the angle of the Right Shoulder
        Right_Shoulder = detector.findAngle(img, 14, 12, 24, height=40, width=-30, show_angle=False)

        # Body alignement
        Body_angle = detector.findAngle(img, 12, 24, 26, height=50, width=80)

        # Angle of right knee
        Knee_angle = detector.findAngle(img, 24, 26, 28, height=50, width=80, show_angle=True)

        # Body perfect straight line
        detector.StraightBodyLine(img, 12, 28)

        per = np.interp(Right_elbow, (75, 160), (0, 100))
        bar = np.interp(Right_elbow, (75, 160), (650, 100))

        # Check to ensure right form before starting the program
        if Right_elbow > 160 and Right_Shoulder > 40 and Body_angle > 160:
            form = 1

        # Check the direction and counts push up
        color = (0, 0, 255)
        # Check for full range of motion for the pushup
        if form == 1:
            if per == 0:
                if Right_elbow <= 90 and Body_angle > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"

            if per == 100:
                if Right_elbow > 160 and Right_Shoulder > 40 and Body_angle > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                    # form = 0

        up_arrow(img=img)
        colorful_up_arrow(img=img, percentage=per)
        cv2.putText(img, f'{int(per)} %', (120, 430), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
        cv2.putText(img, 'UP', (70, 600), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)

        down_arrow(img=img)
        colorful_down_arrow(img=img, percentage=100-per)
        cv2.putText(img, 'DOWN', (1100, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
        cv2.putText(img, f'{int(100-per)} %', (1050, 430), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)

        # Error graph
        cv2.line(img, (450, 100), (1000, 100), (0, 0, 255), 2)

        error_body_angle = int((180 - Body_angle) * 1.5)
        error_knee_angle = int((Knee_angle - 180) * 1.5)

        cv2.circle(img, (450, 100), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (450, 100), 7, (255, 0, 255), 2)

        cv2.circle(img, (550, 100+error_knee_angle), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (550, 100+error_knee_angle), 7, (255, 0, 255), 2)

        cv2.line(img, (450, 100), (550, 100+error_knee_angle), (0, 255, 0), 2)

        cv2.line(img, (550, 100+error_knee_angle), (750, 100-error_body_angle), (0, 255, 0), 2)

        cv2.circle(img, (750, 100-error_body_angle), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (750, 100-error_body_angle), 7, (255, 0, 255), 2)

        cv2.circle(img, (1000, 100), 4, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (1000, 100), 7, (255, 0, 255), 2)

        cv2.line(img, (750, 100-error_body_angle), (1000, 100), (0, 255, 0), 2)

        # Show the error
        cv2.rectangle(img, (220, 190), (510, 240), (100, 0, 0), 1)
        cv2.putText(img, 'Body staright error:     %', (240, 210), cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 100, 0), 2)
        cv2.putText(img, f'{round(((180 - Body_angle) / 180) * 100)}', (440, 210), cv2.FONT_HERSHEY_PLAIN, 1.1,
                    (0, 100, 0), 2)
        cv2.putText(img, 'Knee staright error:     %', (240, 230), cv2.FONT_HERSHEY_PLAIN, 1.1, (0, 100, 0), 2)
        cv2.putText(img, f'{abs(round(((180 - Knee_angle) / 180) * 100))}', (440, 230), cv2.FONT_HERSHEY_PLAIN, 1,
                    (0, 100, 0), 2)

        # Draw Push-Up Counter
        cv2.rectangle(img, (0, 0), (220, 185), (0, 100, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (70, 120), cv2.FONT_HERSHEY_PLAIN, 7, (255, 255, 255), 6)
        cv2.putText(img, 'Push up', (10, 160), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime
    # cv2.putText(img, str(int(fps)), (50, 400), cv2.FONT_HERSHEY_PLAIN, 5,
    #             (255, 0, 0), 5)

    cv2.imshow("Image", img)
    out.write(img)
    cv2.waitKey(1)
