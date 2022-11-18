
import numpy as np #Math
import cv2 #Camera ressources
import imutils  #Image modification
import mediapipe as mp #IA

#Config mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

video_capture_1 = cv2.VideoCapture(2) #Link port cam 1 
video_capture_2 = cv2.VideoCapture(4) #Link port cam 2

def image_to_skeletton(image):
    with mp_holistic.Holistic(min_detection_confidence=0.5,min_tracking_confidence=0.5) as holistic:
    
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
    
        # Draw landmark annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        return cv2.flip(image, 1)

while True:
    
    #Capture frame by frame
    ret1, frame1 = video_capture_1.read()
    ret2, frame2 = video_capture_2.read()
    frame1=cv2.resize(frame1,(256,144))
    frame2=cv2.resize(frame1,(256,144))

    if (ret1):
        # Display the resulting frame on display 1 
        cv2.imshow('Cam 1', image_to_skeletton(frame1))
    
    if (ret2):
        # Display the resulting frame on display 2
        cv2.imshow('Cam 2', image_to_skeletton(frame2))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Close the instance when q is pressed^
video_capture_1.release()
video_capture_2.release()
cv2.destroyAllWindows()

