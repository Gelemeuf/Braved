
#import numpy as np #Math
import cv2 #Camera ressources
import mediapipe as mp #IA
from threading import Thread
from queue import Queue

#Config mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

width = 1920/2
height = 1080/2

class CameraCaptureThread(Thread):
    def __init__(self, id, name, image_queue):
        super().__init__()
        self.id = id
        self.name = name
        self.image_queue = image_queue
        self.cap = cv2.VideoCapture(self.id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, width)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                self.image_queue.put((self.name, frame))
            else:
                break
        self.cap.release()

class CameraViewerThread(Thread):
    def __init__(self, image_queue):
        super().__init__()
        self.image_queue = image_queue

    def run(self):
        while True:
            name, frame = self.image_queue.get()
            cv2.imshow(name, frame)
            # do something with the array
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

class IaThread(Thread):
    def __init__(self,image_queue,array_queue):
        super().__init__()
        self.image_queue = image_queue
        self.array_queue = array_queue
        
    def run(self):
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:

            name, image = self.image_queue.get()
            
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
        
            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            coord=[]
            if results.pose_landmarks:
                for lm in results.pose_landmarks.landmark:   
                    coord.append(0)
                    #coord.append(lm.x,lm.y,lm.z)
                    print("yep")
        self.array_queue.put((name, coord))
        
class Angular_Calcul(Thread):
    def __init__(self,array_queue,angular_queue):
        super().__init__()
        self.array_queue = array_queue
        self.angular_queue = angular_queue
    
image_queue = Queue()
array_queue = Queue()
angular_results = Queue()

thread1 = CameraCaptureThread(2, "Camera 1", image_queue)
#thread2 = CameraCaptureThread(4, "Camera 2", image_queue)
thread1.start()
#thread2.start()

viewer = CameraViewerThread(image_queue)
ia = IaThread(image_queue,array_queue)
angular_calcul = Angular_Calcul(array_queue,angular_results)

viewer.start()
ia.start()
