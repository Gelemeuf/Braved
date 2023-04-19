# Author : Tanguy RIDREMONT
# Date : 14/03/2023
# File : Package to coroborate the pos from the two cams

import math, socket, time
import cv2, sys
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from Data_traitment import *
from display_functions import print_ascii_art

# Video capture variables
videoWidth = 960
videoHeight = 480

# Socket connection
host, port = ('localhost', 1234)
interprogramComm = None

def vectCoord(P1, P2):
    """Return the coordinates of a vector defined by two points"""
    x = P2[0]-P1[0]
    y = P2[1]-P1[1]
    z = P2[2]-P1[2]
    return [x, y, z]

def middlePoint(P1, P2):
    """Return the coordinate of the middle point between two points"""
    x = (P1[0]+P2[0])/2
    y = (P1[1]+P2[1])/2
    z = (P1[2]+P2[2])/2
    return [x, y, z]

def vectLength(vect):
    """Return the length of a given vector"""
    return math.sqrt(vect[0]**2 + vect[1]**2 + vect[2]**2)

def absolutPos(x1, y1, x2, y2):
    """Return the position of a point based on the coordinate from the 2 cameras"""
    x = x1
    y = (y1 + y2)/2
    z = x2
    return [x, y, z]

def vectAngle(vect1, vect2):
   """Return the angle between two vectors"""
   if (vectLength(vect1)*vectLength(vect2) == 0):
      return -1
   else:
      return math.acos((vect1[0]*vect2[0]+vect1[1]*vect2[1]+vect1[2]*vect2[2]) / (vectLength(vect1)*vectLength(vect2)))

def isAbove(P1, P2, P3):
    """Return True if P3 is above the predicted position from the line between P1 and P2"""
    if (P2[0]-P1[0] == 0):
        a = 1
    else:
        a = (P2[1]-P1[1])/(P2[0]-P1[0])
    b = P1[1] - a*P1[0]

    P12 = middlePoint(P1, P2)
    distance = vectLength([P3[0]-P12[0], P3[1]-P12[1], 0])

    if (P3[1] > (a*P3[0]+b)):
        return [True, distance]
    else:
        return [False, distance]

def isInfront(P1, P2, P3):
    """Return True if P3 is in front of the line between P1 and P2"""
    if ((P2[0]-P1[0]) == 0):
        a = 1
    else:
        a = (P2[2]-P1[2])/(P2[0]-P1[0])
    b = P1[2] - a*P1[0]

    P12 = middlePoint(P1, P2)

    distance = vectLength([P3[0]-P12[0], 0, P3[2]-P12[2]])

    if (P3[2] < (a*P3[0]+b)):
       return [False, distance]
    else:
        return [True, distance]

def angleCalculation(coord):
    angles1 = [0, 0, 0, 0, 0, 0]
    angles2 = [0, 0, 0, 0, 0, 0]

    # Spine vector down to up
    vect1234 = vectCoord(middlePoint(coord[11], coord[12]), middlePoint(coord[23], coord[24]))

    # Shoulder line vector
    vect1112 = vectCoord(coord[11], coord[12])
    vect1211 = vectCoord(coord[12], coord[11])

    # Upper arm vectors
    vect1113 = vectCoord(coord[11], coord[13])
    vect1214 = vectCoord(coord[12], coord[14])

    # Forearm vectors
    vect1315 = vectCoord(coord[13], coord[15])
    vect1416 = vectCoord(coord[14], coord[16])

    # Hand vectors
    vect1579 = vectCoord(coord[13], middlePoint(coord[17], coord[19]))
    vect1680 = vectCoord(coord[16], middlePoint(coord[18], coord[20]))

    # Hand rotation
    vect1719 = vectCoord(coord[17], coord[19])
    vect1820 = vectCoord(coord[18], coord[20])

    # Angle 1 calculation (formules correctes)
    angles1[0] = -(vectAngle(vect1234, vect1315) - (math.pi/2))
    angles2[0] = vectAngle(vect1234, vect1416) - (math.pi/2)

    # Angle 2 calculation
        # First calculation method
    front1 = isInfront(coord[11], coord[12], coord[13])
    front1[1] = abs(front1[1])
    above1 = isAbove(coord[11], coord[12], coord[13])
    above1[1] = abs(above1[1])
    total1 = front1[1] + above1[1]
    if total1 == 0:
        total1 = 10
    horizontal1 = front1[1]/total1
    vertical1 = above1[1]/total1

    if front1[0]:
        angles1[1] = vectAngle(vect1113, vect1112) - math.pi
    else:
        angles1[1] = math.pi - vectAngle(vect1113, vect1112)
    if above1[0]:
        angles1[1] = angles1[1]*horizontal1 + (vectAngle(vect1113, vect1112) - math.pi)*vertical1
    else:
        angles1[1] = angles1[1]*horizontal1 + (math.pi - vectAngle(vect1113, vect1112))*vertical1

    front2 = isInfront(coord[12], coord[11], coord[14])
    front2[1] = abs(front2[1])
    above2 = isAbove(coord[12], coord[11], coord[14])
    above2[1] = abs(above2[1])
    total2 = front2[1] + above2[1]
    horizontal2 = front2[1]/total2
    vertical2 = above2[1]/total2
    if front2[0]:
        angles2[1] = vectAngle(vect1214, vect1211) - math.pi
    else:
        angles2[1] = math.pi - vectAngle(vect1214, vect1211)
    if above2[0]:
        angles2[1] = angles2[1]*horizontal2 + (vectAngle(vect1214, vect1112) - math.pi)*vertical2
    else:
        angles2[1] = angles2[1]*horizontal2 + (math.pi - vectAngle(vect1214, vect1211))*vertical2

        # Second calculation method
    # horizontal1 = math.pi/4 - abs(angles2[0])
    # vertical1 = abs(angles2[0])
    # if front1[0]:
        # angles1[1] = vectAngle(vect1113, vect1112) - math.pi
    # else:
        # angles1[1] = math.pi - vectAngle(vect1113, vect1112) 
    # if above1[0]:
        # angles1[1] = angles1[1]*horizontal1 + (vectAngle(vect1113, vect1112) - math.pi)*vertical1
    # else:
        # angles1[1] = angles1[1]*horizontal1 + (math.pi - vectAngle(vect1113, vect1112))*vertical1

    # Angle 3 calculation (formules correctes)
    angles1[2] = math.pi/2 - vectAngle(vect1113, vect1315)
    angles2[2] = math.pi/2 - vectAngle(vect1214, vect1416)

    # # Angle 4 calculation - Formules imprécises
    angles1[3] = vectAngle([vect1719[0], 0, vect1719[2]], vect1719)
    angles2[3] = vectAngle([vect1820[0], 0, vect1820[2]], vect1820)

    # # Angle 5 calculation - Formules imprécises
    angles1[4] = vectAngle(vect1315, vect1579)
    angles2[4] = vectAngle(vect1416, vect1680)

    # Angle 6 calculation
    # angles1[5] = 0
    # angles2[5] = 0

    return [angles1, angles2]

# Main program
if __name__ == "__main__":

    print_ascii_art("DispLogo.png", 10, 0.01)

    print("#######################################")
    print("#        Camera program started       #")
    print("#######################################\n")

    # Socket connection
    host, port = ('localhost', 1234)
    interprogramComm = None

    try:
        interprogramComm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        interprogramComm.connect((host, port))
        print(">>> Connection to the data traitment program is a success")
    except:
        print(">>> Connection to the data traitment program failed")
        print("#######################################")
        print("#       Camera program stopped        #")
        print("#######################################")
        sys.exit()

    answer = "0"
    while answer not in ['Y', 'N']:
        answer = input("Do you want to show the camera feed (Y/N) : ")

    Angles = [[0., 0., 0., 0., 0., 0.], [0., 0., 0., 0., 0., 0.]]

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)

    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, videoWidth)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, videoHeight)
    cap2.set(cv2.CAP_PROP_FRAME_WIDTH, videoWidth)
    cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, videoHeight)

    coord = list()
    coord1 = list()
    coord2 = list()
    for i in range(0, 33):
       coord.append([0, 0, 0])
       coord1.append([0, 0])
       coord2.append([0, 0])

    while True:

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            if (cap1.isOpened() and cap2.isOpened()):
                success1, image1 = cap1.read()
                success2, image2 = cap2.read()
                if not success1:
                    print("Ignoring empty camera1 frame.")
                    continue
                if not success2:
                    print("Ignoring empty camera2 frame.")
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image1.flags.writeable = False
                image2.flags.writeable = False
                image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
                image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
                results1 = pose.process(image1)
                results2 = pose.process(image2)

                # Draw the pose annotation on the image.
                image1.flags.writeable = True
                image2.flags.writeable = True
                image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
                image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR)

                mp_drawing.draw_landmarks(image1, results1.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                mp_drawing.draw_landmarks(image2, results2.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                posX = list()
                posY = list()
                posZ = list()

                if results1.pose_world_landmarks:
                   for id, lm in enumerate(results1.pose_world_landmarks.landmark):
                        coord1[id] = [-lm.x, -lm.y]
                if results2.pose_world_landmarks:
                    for id, lm in enumerate(results2.pose_world_landmarks.landmark):
                        coord2[id]  = [-lm.x, -lm.y]

                for id in range(len(coord)):
                    coord[id] = absolutPos(coord1[id][0], coord1[id][1], coord2[id][0], coord2[id][1])

                Angles = angleCalculation(coord)

                if answer == "Y":
                    cv2.imshow('Cam1', cv2.flip(image1, 1))
                    cv2.imshow('Cam2', cv2.flip(image2, 1))
                if cv2.waitKey(5) & 0xFF == 27:
                  break
        msgAI = prepareDatas("AI", Angles[1])
        try:
            interprogramComm.send(bytes(msgAI, "utf-8"))
        except:
            print(">>> No data could be sent")
            break
        time.sleep(WaitTime)

    cap1.release()
    cap2.release()

    if interprogramComm != None:
        print(">>> Closing connection to data traitment program\n")
        interprogramComm.close()

    print("#######################################")
    print("#       Camera program stopped        #")
    print("#######################################")