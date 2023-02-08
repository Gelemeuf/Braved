# Project 14 : Controling a robotic arm using VR
# Modification date : 12/12/2022 - Tanguy
# File : Control robot's mouvements


# Importing needed librairies
from pyniryo import *
import sys, keyboard, time
from Arm_Kinematic import *


# Variables
KeyWaitTime = 0
pasDeplacement = 4


# Useful variables for robot connection
robotAddress_WiFi= "10.10.10.10"                    # Default IP address for a WiFi use of the robot
robotAddress_Ethernet = "169.254.200.200"           # Default IP address for a ethernet use of the robot
robot = None                                        # When robot isn't connected


# Declaration of object used in the project
class Joint:
    """Describe one of the 6 robot's joint"""

    name = "Unbound joint"
    askedPosition = 0
    actualPosition = 0
    minValue = 0
    maxValue = 0

    def __init__(self, name, askedPosition, extremeValue) -> None:
        """param
        name : str
        initialPosition : float
        extremeValue : list (size=2)"""
        self.name = name
        self.askedPosition = askedPosition
        self.minValue, self.maxValue = extremeValue[0], extremeValue[1]
        pass


def getAskedJointPosList(joints):
    """Return a list which is the argument for the move_joints function"""
    result = list()
    for joint in joints:
        result.append(joint.askedPosition)
    return result

def updateAskedPos(joinPos, Joints):
    """Update Joints value with the input from the user"""
    for i in range(6):
        if (joinPos[i] > Joints[i].minValue) and (joinPos[i] < Joints[i].maxValue):
            Joints[i].askedPosition = joinPos[i]
        else:
            print(f"Joint n°{i} can move this far ({joinPos[i]} rads)")

def updateActualPos(robot, robotsJoints):
    """Get all the position from robots joints"""
    actPosList = robot.get_joints()
    for i in range(6):
        robotsJoints[i].actualPosition = actPosList[i]


if (__name__ == "__main__"):
    # Connect to robot
    answer = input("Choose the selected connection methode : ")
    try:
        if (answer == "wifi"):
            robot = NiryoRobot(robotAddress_WiFi)
        elif (answer == "ethernet"):
            robot = NiryoRobot(robotAddress_Ethernet)
        else:
            robot = NiryoRobot(input("Enter robot's IP address : "))
    except:
        sys.exit()
    robot.calibrate_auto()

    robot.set_jog_control(enabled=True)

    # Defining  all joints
    joint1 = Joint("shoulderRotation", 0, [-2.867, 2.867])
    joint2 = Joint("shoulderIncline", 0, [-1.99, 0.51])
    joint3 = Joint("elbowIncline", 0, [-1.24, 1.47])
    joint4 = Joint("elbowRotation", 0, [-1.994, 1.994])
    joint5 = Joint("wristIncline", 0, [-1.994, 0.947])
    joint6 = Joint("wristRotation", 0, [-2.431, 2.431])

    robotsJoints = [joint1, joint2, joint3, joint4, joint5, joint6]

    # Controling robot
    Choosed_session = 0
    End_session = False

    answer = input("Choose the operation mode : ")

    if (answer == "Angles"):
        Choosed_session = 1
    else:
        Choosed_session = 0

    if (Choosed_session == 1):
        while not (End_session):
            answer = input("Enter orders : ")
            if (answer == "quit"):
                robot.close_connection()
                sys.exit()
            elif (answer == "home"):
                robot.move_to_home_pose()
            elif (answer == "open"):
                robot.release_with_tool()
            elif (answer == "close"):
                robot.grasp_with_tool()
            elif (answer == "velocity"):
                answer = int(input("Enter velocity (percentage of max speed) : "))
                if (answer > 100) or (answer < 0):
                    print("The velocity is a percentage of max. It should be between 0 and 100 %")
                else:
                    robot.set_arm_max_velocity(answer)
            elif (answer == "display"):
                joints = getAskedJointPosList(robotsJoints)[0:3]
                joints[1] = joints[1] + math.pi/2
                joints[2] = joints[2] - math.pi/2 + joints[1]
                displayEstimatePos(joints)
            else:
                listJoint = list(float(i) for i in answer.split(","))
                updateAskedPos(listJoint, robotsJoints)
                updateActualPos(robot, robotsJoints)
                robot.jog_joints(getAskedJointPosList(robotsJoints))
    else:
        WantedPos = PoseObject(x=24, y=0, z=22.5, roll=0, pitch=0, yaw=0)
        while not(End_session):
            key = keyboard.read_key()
            if key == "x":
                End_session = True
            elif key == "z":
                WantedPos.x += pasDeplacement
                time.sleep(KeyWaitTime)
            elif key == "s":
                WantedPos.x -= pasDeplacement
                time.sleep(KeyWaitTime)
            elif key == "q":
                WantedPos.y += pasDeplacement
                time.sleep(KeyWaitTime)
            elif key == "d":
                WantedPos.y -= pasDeplacement
                time.sleep(KeyWaitTime)
            elif key == "space":
                WantedPos.z += pasDeplacement
                time.sleep(KeyWaitTime)
            elif key == "o":
                robot.release_with_tool()
                time.sleep(KeyWaitTime)
            elif key == "e":
                robot.grasp_with_tool()
                time.sleep(KeyWaitTime)
            elif key == "v":
                WantedPos.z -= pasDeplacement
                time.sleep(KeyWaitTime)
            elif key == "gauche":
                WantedPos.roll += pasDeplacement
                time.sleep(KeyWaitTime)
            elif key == "droite":
                WantedPos.roll -= pasDeplacement
                time.sleep(KeyWaitTime)
            elif key == "haut":
                WantedPos.pitch += pasDeplacement
                time.sleep(KeyWaitTime)
            elif key == "bas":
                WantedPos.pitch -= pasDeplacement
                time.sleep(KeyWaitTime)
            elif key == "p":
                joints = getAskedJointPosList(robotsJoints)[0:3]
                joints[1] = joints[1] + math.pi/2
                joints[2] = joints[2] - math.pi/2 + joints[1]
                displayEstimatePos(joints)          
            else:
                pass

            if key in ["z", "s", "q", "d", "space", "v", "gauche", "droite", "haut", "bas"]:
                if (isReachable(WantedPos.x, WantedPos.y, WantedPos.z, upperArmLength, forearmLength)):
                    joints = getAskedJointPosList(robotsJoints)
                    joints[1] = joints[1] + math.pi/2
                    joints[2] = joints[2] - math.pi/2 + joints[1]
                    angles = list(angleCalculation(WantedPos.x, WantedPos.y, WantedPos.z, joints[0], joints[1], joints[2]))
                    angles[1] = angles[1] - math.pi/2
                    angles[2] = angles[2] - angles[1]
                    for i in range(3):
                        angles.append(0.)
                    updateAskedPos(angles, robotsJoints)
                    print(getAskedJointPosList(robotsJoints))         
                    updateActualPos(robot, robotsJoints)
                    robot.move_joints(getAskedJointPosList(robotsJoints))

    # End connection when the program ends
    try:
        robot.close_connection()
    except:
        pass
