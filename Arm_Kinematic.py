# Project 14 : Controling a robotic arm using VR
# Modification date : 07/02/2022 - Tanguy
# File : Display a given position

# Importing the needed librairies
import time, math, sys, socket
import numpy as np
import matplotlib.pyplot as plt
import select
from tkinter import messagebox
from Data_traitment import *
from display_functions import print_ascii_art

# Robot's component size
upperarmLength = 22.5
forearmLength = 24
gripperSize = 5
opened = 1

Reach = upperarmLength + forearmLength + 8

# Defining the angle from robot's joints
AiPos = [0., 0., 0., 0., 0., 0.]
RobotPos = [0., 0., 0., 0., 0., 0.]

def plotRobot(axis, angles, color):
    # Define the matrix to model the robot
    rep01 = np.array([[np.cos(angles[0]), -np.sin(angles[0]), 0], [np.sin(angles[0]), np.cos(angles[0]), 0], [0, 0, 1]])
    rep12 = np.array([[1, 0, 0], [0, np.cos(angles[1]), -np.sin(angles[1])], [0, np.sin(angles[1]), np.cos(angles[1])]])
    rep23 = np.array([[0], [0], [upperarmLength]])
    rep34 = np.array([[1, 0, 0], [0, np.cos(angles[2]), -np.sin(angles[2])], [0, np.sin(angles[2]), np.cos(angles[2])]])
    rep45 = np.array([[np.cos(angles[3]), 0, -np.sin(angles[3])], [0, 1, 0], [np.sin(angles[3]), 0, np.cos(angles[3])]])
    rep56 = np.array([[0], [forearmLength], [0]])
    rep67 = np.array([[1, 0, 0], [0, np.cos(angles[4]), -np.sin(angles[4])], [0, np.sin(angles[4]), np.cos(angles[4])]])
    rep78 = np.array([[np.cos(angles[5]), 0, -np.sin(angles[5])], [0, 1, 0], [np.sin(angles[5]), 0, np.cos(angles[5])]])

    # Calculate the coordinates of robot's joints
    O0 = np.array([[0], [0], [0]])
    O1 = rep01.dot( rep12.dot( rep23 + np.array([[0], [0], [0]]) ) )
    O2 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + np.array([[0], [0], [0]]) ) ) ) ) )
    O3 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + rep67.dot( rep78.dot( np.array([[0], [2], [0]]) ) ) ) ) ) ) )
    O4 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + rep67.dot( rep78.dot( np.array([[gripperSize/2], [2], [0]]) ) ) ) ) ) ) )
    O5 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + rep67.dot( rep78.dot( np.array([[-gripperSize/2], [2], [0]]) ) ) ) ) ) ) )
    O6 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + rep67.dot( rep78.dot( np.array([[(gripperSize/2)*opened], [6], [0]]) ) ) ) ) ) ) ) 
    O7 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + rep67.dot( rep78.dot( np.array([[(-gripperSize/2)*opened], [6], [0]]) ) ) ) ) ) ) )

    # Plot the points and the lines
    scatterPoints = [O0, O1, O2, O3, O4, O5, O6, O7]
    posX = list()
    posY = list()
    posZ = list()
    for point in scatterPoints:
        posX.append(point[0][0])
        posY.append(point[1][0])
        posZ.append(point[2][0])
    for i in range(len(posX)-3):
        axis.plot([posX[i], posX[i+1]], [posY[i], posY[i+1]], [posZ[i], posZ[i+1]], "#000000")
    axis.plot([posX[4], posX[6]], [posY[4], posY[6]], [posZ[4], posZ[6]], "#000000")
    axis.plot([posX[5], posX[7]], [posY[5], posY[7]], [posZ[5], posZ[7]], "#000000")
    # Add text to the plot
    axis.set_xlim(-Reach, Reach)
    axis.set_xlabel("X-axis")
    axis.set_ylim(-Reach, Reach)
    axis.set_ylabel("Y-axis")
    axis.set_zlim(-Reach, Reach)
    axis.set_zlabel("Z-axis")
    
    axis.scatter(posX, posY, posZ, color=color, s=40)

if __name__ == "__main__":
    isActive = 1
    error = 0

    print_ascii_art("DispLogo.png", 10, 0.01)

    print("#######################################")
    print("#     Vizualisation has awakend       #")
    print("#######################################\n")

    # Socket connection
    host, port = ('localhost', 1234)
    interprogramComm = None

    try:
        interprogramComm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        interprogramComm.connect((host, port))
        print(">>> Connection to the data traitment program is a success")
    except:
        print("Connection to the data traitment program failed")
        sys.exit()

    # Create the plot
    figure = plt.figure()
    axis = figure.add_subplot(projection='3d')

    while True:
        try:
            ready = select.select([interprogramComm], [], [], 0.01)
            if ready[0]:
                msg = interprogramComm.recv(1024).decode("utf-8")
                datas = dataTraitment(msg)
                if datas[0] != -1:
                    error = 0
                    if datas[0] == "AI":
                        AiPos = datas[1]
                    if datas[0] == "Robot":
                        RobotPos = datas[1]
                else:
                    error += 1
        except:
            print(">>> Error while receiving data")
            break
        if error > 10:
            plt.close('all')
            print(">>> No response from the data traitment program")
            break

        # Plot the form of the robot
        if len(AiPos) == 6:
            plotRobot(axis, AiPos, "#FF0000")
        if len(RobotPos) == 6:
            plotRobot(axis, RobotPos, "#0000FF")
        plt.pause(0.01)
        axis.cla()
    
    # Ploting robot's joints


    # Leave the programme
    plt.show()

    if interprogramComm != None:
        print(">>> Closing connection to data traitment program\n")
        interprogramComm.close()

    print("#######################################")
    print("#   Vizualisation returns to ashes    #")
    print("#######################################")
    sys.exit()