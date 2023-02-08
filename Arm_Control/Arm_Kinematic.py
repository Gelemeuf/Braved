# Project 14 : Controling a robotic arm using VR
# Modification date : 12/12/2022 - Tanguy
# File : Calculate robot's mouvements by x,y,z

# Needed librairies
import math
import matplotlib.pyplot as plt
import scipy.optimize as op

# Arm's lengths
upperArmLength = 22.5   # Size of the segment between shoulder and elbow
forearmLength = 24      # Size of the segment between elbow and wrist articulation

# Coordinates
wantedX = 20
wantedY = 20
wantedZ = 20

# Initiale values
theta0Init = math.pi/4
theta1Init = math.pi/2
theta2Init = math.pi/4

def maxReach(t1, t2):
    """Calculate the maximum distance that the arm can reach
    
    :param
    t1: float, size of the first segment
    t2 : float, size of the second segment

    :return
    float, sum of the two parameters"""
    return t1+t2

def isReachable(x, y, z, t1, t2):
    """Define if the arm can reach the selected coordinates
    
    :param
    x : float, coordinate to reach
    y : float, coordinate to reach
    z : float, coordinate to reach
    t1 : float, size of the first segment
    t2 : float, size of the seconde segment

    :return
    bool, the coordinates are reachable with the arm"""
    Reach = maxReach(t1, t2)
    return (Reach > math.sqrt(x**2 + y**2 + z**2))

def funct(thetas):
    """Return the difference between the wanted coordinates and the coordinates that the arm reaches with its angles
    
    :param
    thetas : list, contains the 3 angles of the arm
    
    :return
    list, contains the difference in coordinates"""
    global wantedX, wantedY, wantedZ
    return [wantedX - (upperArmLength*math.cos(thetas[1]) + forearmLength*math.cos(thetas[2]))*math.cos(thetas[0]),
    wantedY - (upperArmLength*math.cos(thetas[1]) + forearmLength*math.cos(thetas[2]))*math.sin(thetas[0]),
    wantedZ - (upperArmLength*math.sin(thetas[1]) + forearmLength*math.sin(thetas[2]))
    ]

def angleCalculation(x, y, z, o1, o2, o3):
    """Solve the system to calculate angle based on the wanted coordinates
    
    :param
    x : float, wanted coordinates for x axis
    y : float, wanted coordinates for y axis
    z : float, wanted coordinates for z axis
    o1 : float, angle 1 from which the system starts
    o2 : float, angle 2 from which the system starts
    o3 : float, angle 3 from which the system starts
    
    :return
    list, contains the calculated angles needed to reach the coordinates"""
    global wantedX, wantedY, wantedZ
    wantedX = x
    wantedY = y
    wantedZ = z
    return op.fsolve(funct, (o1, o2, o3))

def displayEstimatePos(thetas):
    """Display in Matplot the position of the arm based on the angle of its joints
    
    :param
    thetas : list, contains the angle of the differents joints of the arm"""
    print(thetas)
    x0 = 0
    y0 = 0
    z0 = 0

    x1 = upperArmLength*math.cos(thetas[1])*math.cos(thetas[0])
    y1 = upperArmLength*math.cos(thetas[1])*math.sin(thetas[0])
    z1 = upperArmLength*math.sin(thetas[1])


    x2 = forearmLength*math.cos(thetas[2])*math.cos(thetas[0]) + x1
    y2 = forearmLength*math.cos(thetas[2])*math.sin(thetas[0]) + y1
    z2 = forearmLength*math.sin(thetas[2]) + z1

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.plot([x0, x1], [y0, y1], [z0, z1], "black")
    ax.plot([x1, x2], [y1, y2], [z1, z2], "black")

    ax.scatter(x0, y0, z0, s=100, marker=".")
    ax.scatter(x1, y1, z1, s=100, marker=".")
    ax.scatter(x2, y2, z2, s=100, marker=".")

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    Reach = maxReach(upperArmLength, forearmLength)
    ax.set_xlim3d(-Reach, Reach)
    ax.set_ylim3d(-Reach, Reach)
    ax.set_zlim3d(-Reach, Reach)

    plt.title("Arm projection")
    plt.show()

if (__name__ == "__main__"):
    wantedX = 20
    wantedY = 20
    wantedZ = 14
    if isReachable(wantedX, wantedY, wantedZ, upperArmLength, forearmLength):
        thetas = angleCalculation(wantedX, wantedY, wantedZ, theta0Init, theta1Init, theta2Init)
        displayEstimatePos(thetas)
