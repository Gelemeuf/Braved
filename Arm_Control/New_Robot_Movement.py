# Project 14 : Controling a robotic arm using VR
# Modification date : 19/01/2023 - Tanguy
# File : Control robot's mouvements


# Importing needed librairies
from pyniryo import *
import time, sys
import matplotlib.pyplot as plt
import pid_API as PID
from Arm_Kinematic import *

# Useful variables for robot connection
robotAddress_WiFi= "10.10.10.10"                    # Default IP address for a WiFi use of the robot
robotAddress_Ethernet = "169.254.200.200"           # Default IP address for a ethernet use of the robot
robot = None                                        # When robot isn't connected

# Declaration of object used in the project
class Joint:
    """Describe one of the robot's joints"""

    name = "Unbound joint"
    number = 0
    askedPosition = 0
    minValue = 0
    maxValue = 0
    security = 0
    PID = PID.PID(0, 0, 0, [0, 0])

    def __init__(self, name, number, askedPosition, extremeValue, pid):
        """param
        name : str
        initialPosition : float
        extremeValue : list (size=2)"""
        self.name = name
        self.number = number
        self.askedPosition = askedPosition
        self.minValue, self.maxValue, self.security = extremeValue[0], extremeValue[1], extremeValue[2]
        self.PID = PID.PI(pid[0], pid[1], pid[2])

    def update_pos(self, value):
        if (value>self.minValue) and (value<self.maxValue):
            self.askedPosition = value


# Function to update
def getAskedJointPosList(joints):
    """Return a list which is the argument for the move_joints function"""
    result = list()
    for joint in joints:
        result.append(joint.askedPosition)
    return result


def updateAskedPos(joinPos, Joints):
    """Update Joints value with the input from the user"""
    for i in range(6):
        if (joinPos[i] > Joints[i].minValue+Joints[i].security) and (joinPos[i] < Joints[i].maxValue-Joints[i].security):
            Joints[i].askedPosition = joinPos[i]
        else:
            print(f"Joint n°{i} can move this far ({joinPos[i]} rads)")


def updateActualPos(robot, robotsJoints):
    """Get all the position from robots joints"""
    actPosList = robot.get_joints()
    for i in range(6):
        robotsJoints[i].actualPosition = actPosList[i]


# Main program
if (__name__ == "__main__"):
    # Connect to robot
#    answer = input("Choose the selected connection methode : ")
#    try:
#        if (answer == "wifi"):
#            robot = NiryoRobot(robotAddress_WiFi)
#        elif (answer == "ethernet"):
#            robot = NiryoRobot(robotAddress_Ethernet)
#        else:
#            robot = NiryoRobot(input("Enter robot's IP address : "))
#    except:
#        sys.exit()

    robot = NiryoRobot(robotAddress_Ethernet)
    
    robot.calibrate_auto()
    robot.move_to_home_pose()
    robot.set_arm_max_velocity = 100
    robot.set_jog_control(enabled=True)

    # Defining  all joints
    joint1 = Joint("shoulderRotation", 1, 0, [-2.6, 2.6, 0.2], [0.03, 0.0002, 0, [0,0]])
    joint2 = Joint("shoulderIncline", 2, 0, [-1.4, 0.45, 0.2], [0.08, 0.0002, 0, [0,0]])
    joint3 = Joint("elbowIncline", 3, 0, [-1.1, 1.3, 0.2], [0.07, 0.0001, 0, [0,0]])
    joint4 = Joint("elbowRotation", 4, 0, [-1.994, 1.994, 0.2], [0, 0, 0, [0,0]])
    joint5 = Joint("wristIncline", 5, 0, [-1.7, 0.9, 0.2], [0.1, 0.0002, 0, [0,0]])
    joint6 = Joint("wristRotation", 6, 0, [-2.431, 2.431, 0.2], [0.17, 0.0002, 0, [0,0]])

    robotsJoints = [joint1, joint2, joint3, joint4, joint5, joint6]

    cmd = [0,0,0,0,0,0]

    t = time.time()
    start = t
    t_next = 0

    move = [0,0,0,0,0,0]
    
    while (True):
        values = robot.get_joints()

        t_next = time.time()
        dt = t_next - t

        for i in range(6):
            move[i] = robotsJoints[i].PID.calcul(cmd[i], values[i], dt)

        robot.jog_joints(move)

        t = t_next
