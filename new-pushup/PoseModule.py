import cv2
import mediapipe as mp
import time
import math


class poseDetector:

    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):

        self.model_complexity = 2
        self.lmList = None
        self.results = None

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.upBody, self.smooth,
                                     self.detectionCon, self.trackCon)

    # This method is to find and draw the landmarks
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    # This method is to return the list containe the id and the coordinates of all the landmarks
    def land_mark_list(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for Id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([Id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return self.lmList

    # This method is to calculate the mesure of an angle between three landmarks
    def findAngle(self, img, p1, p2, p3, height, width, draw=True, show_angle=True):
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 2)
            cv2.circle(img, (x1, y1), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 12, (255, 0, 255), 2)
            cv2.circle(img, (x2, y2), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 12, (255, 0, 255), 2)
            cv2.circle(img, (x3, y3), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 12, (255, 0, 255), 2)

            if show_angle:
                cv2.putText(img, f'{str(int(angle))} degrees', (x2 - width, y2 + height),
                            cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)

        return angle

    def StraightBodyLine(self, img, p1, p2):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]

        cv2.line(img, (x1+20, y1-50), (x2-20, y2-50), (0, 0, 255), 2)
