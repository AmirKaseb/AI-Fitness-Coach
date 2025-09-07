
import cv2
import mediapipe as mp
import math

class poseDetector() :
    
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detectionCon=0.5, trackCon=0.5):
        
        self.mode = mode 
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth_landmarks,
                                     self.enable_segmentation, self.smooth_segmentation,
                                     self.detectionCon, self.trackCon)
        
        
    def findPose (self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
                
        return img
    
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                #finding height, width of the image printed
                h, w, c = img.shape
                #Determining the pixels of the landmarks
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
        return self.lmList
        
    def findAngle(self, img, p1, p2, p3, height=50, width=50, draw=True, show_angle=True):   
        #Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        
        #Calculate Angle
        angle = math.degrees(math.atan2(y3-y2, x3-x2) - 
                             math.atan2(y1-y2, x1-x2))
        if angle < 0:
            angle += 360
            if angle > 180:
                angle = 360 - angle
        elif angle > 180:
            angle = 360 - angle
        # print(angle)
        
        #Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255,255,255), 2)
            cv2.line(img, (x3, y3), (x2, y2), (255,255,255), 2)

            
            cv2.circle(img, (x1, y1), 8, (0,255,0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 12, (255,0,255), 2)
            cv2.circle(img, (x2, y2), 8, (0,255,0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 12, (255,0,255), 2)
            cv2.circle(img, (x3, y3), 8, (0,255,0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 12, (255,0,255), 2)
            
            if show_angle:
                cv2.putText(img, f'{str(int(angle))} degrees', (x2 - width, y2 + height), 
                            cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)
        return angle

    def land_mark_list(self, img, draw=True):
        """Alternative method name for findPosition to match new implementation"""
        return self.findPosition(img, draw)

    def StraightBodyLine(self, img, p1, p2):
        """Draw a straight line between two points to show body alignment"""
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        
        cv2.line(img, (x1+20, y1-50), (x2-20, y2-50), (0, 0, 255), 2)
        

def main():
    detector = poseDetector()
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read() #ret is just the return variable, not much in there that we will use. 
        if ret:    
            img = detector.findPose(img)
            cv2.imshow('Pose Detection', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()