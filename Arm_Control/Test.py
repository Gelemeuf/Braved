import time, math, sys
import numpy as np
import matplotlib.pyplot as plt
import keyboard

upperarmLength = 22.5
forearmLength = 24
gripperSize = 5
opened = 1
isActive = 1

Reach = upperarmLength + forearmLength + 8

o1 = 0
o2 = 0
o3 = 0
o4 = 0
o5 = 0
o6 = 0

figure = plt.figure()
axis = figure.add_subplot(projection='3d')

while(isActive):

    if keyboard.is_pressed('q'):
        isActive = 0

    rep01 = np.array([[np.cos(o1), -np.sin(o1), 0], [np.sin(o1), np.cos(o1), 0], [0, 0, 1]])
    rep12 = np.array([[1, 0, 0], [0, np.cos(o2), -np.sin(o2)], [0, np.sin(o2), np.cos(o2)]])
    rep23 = np.array([[0], [0], [upperarmLength]])
    rep34 = np.array([[1, 0, 0], [0, np.cos(o3), -np.sin(o3)], [0, np.sin(o3), np.cos(o3)]])
    rep45 = np.array([[np.cos(o4), 0, -np.sin(o4)], [0, 1, 0], [np.sin(o4), 0, np.cos(o4)]])
    rep56 = np.array([[0], [forearmLength], [0]])
    rep67 = np.array([[1, 0, 0], [0, np.cos(o5), -np.sin(o5)], [0, np.sin(o5), np.cos(o5)]])
    rep78 = np.array([[np.cos(o6), 0, -np.sin(o6)], [0, 1, 0], [np.sin(o6), 0, np.cos(o6)]])

    o6 = time.time()%(2*math.pi)

    O0 = np.array([[0], [0], [0]])
    O1 = rep01.dot( rep12.dot( rep23 + np.array([[0], [0], [0]]) ) )
    O2 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + np.array([[0], [0], [0]]) ) ) ) ) )
    O3 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + rep67.dot( rep78.dot( np.array([[0], [2], [0]]) ) ) ) ) ) ) )
    O4 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + rep67.dot( rep78.dot( np.array([[gripperSize/2], [2], [0]]) ) ) ) ) ) ) )
    O5 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + rep67.dot( rep78.dot( np.array([[-gripperSize/2], [2], [0]]) ) ) ) ) ) ) )
    O6 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + rep67.dot( rep78.dot( np.array([[(gripperSize/2)*opened], [6], [0]]) ) ) ) ) ) ) ) 
    O7 = rep01.dot( rep12.dot( rep23 + ( rep34.dot( rep45.dot( rep56 + rep67.dot( rep78.dot( np.array([[(-gripperSize/2)*opened], [6], [0]]) ) ) ) ) ) ) )

    scatterPoints = [O0, O1, O2, O3, O4, O5, O6, O7]
    posX = list()
    posY = list()
    posZ = list()
    for point in scatterPoints:
        posX.append(point[0][0])
        posY.append(point[1][0])
        posZ.append(point[2][0])

    for i in range(len(posX)-3):
        axis.plot([posX[i], posX[i+1]], [posY[i], posY[i+1]], [posZ[i], posZ[i+1]], '#000000')
    axis.plot([posX[4], posX[6]], [posY[4], posY[6]], [posZ[4], posZ[6]], '#000000')
    axis.plot([posX[5], posX[7]], [posY[5], posY[7]], [posZ[5], posZ[7]], '#000000')

    axis.set_xlim(-Reach, Reach)
    axis.set_xlabel("X-axis")
    axis.set_ylim(-Reach, Reach)
    axis.set_ylabel("Y-axis")
    axis.set_zlim(-Reach, Reach)
    axis.set_zlabel("Z-axis")

    axis.scatter(posX, posY, posZ, color="#FF0000", s=40)
    plt.pause(0.01)
    axis.cla()

plt.show()
sys.exit()