# Project 14 : Controling a robotic arm using VR
# Modification date : 19/01/2023 - Tanguy
# File : Control robot's mouvements


# Importing needed librairies
from pyniryo import *
import time, sys, socket, select
import matplotlib.pyplot as plt
import pid_API as PID
from Arm_Kinematic import *
from Data_traitment import *
from display_functions import print_ascii_art

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
        if (value>self.minValue+self.security) and (value<self.maxValue-self.security):
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

# Secure the command given to the robot
def securiseCommand(Joints, Command):
    secureCommand = [0., 0., 0., 0., 0., 0.]
    if ((len(Joints)==6) and (len(Command)==6)):
        for i in range(6):
            actCommand = Command[i]
            actJoint = Joints[i]
            if (actCommand < (actJoint.minValue + actJoint.security)):
                secureCommand[i] = Joints[i].minValue + actJoint.security
            elif (actCommand > (actJoint.maxValue - actJoint.security)):
                secureCommand[i] = actJoint.maxValue - actJoint.security
            else:
                secureCommand[i] = actCommand
    return secureCommand

def on_click(x, y, button, pressed):
    if (pressed):
        print(button)

# Main program
if (__name__ == "__main__"):

    print_ascii_art("DispLogo.png", 10, 0.01)

    print("#######################################")
    print("#        Robot control started        #")
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
        print("#        Robot control stopped        #")
        print("#######################################\n")
        sys.exit()

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
        if interprogramComm != None:
            print(">>> Closing connection to data traitment program\n")
            interprogramComm.close()
        print("#######################################")
        print("#        Robot control stopped        #")
        print("#######################################")
        sys.exit()
    
    robot.calibrate_auto()
    robot.move_to_home_pose()
    robot.set_arm_max_velocity = 100
    robot.set_jog_control(enabled=True)

    # Defining  all joints
    joint1 = Joint("shoulderRotation", 1, 0, [-2.6, 2.6, 0.2], [0.06, 0.0002, 0, [0,0]])
    joint2 = Joint("shoulderIncline", 2, 0, [-1, 0.45, 0.2], [0.09, 0.0002, 0, [0,0]]) # Normal angle is -1.4
    joint3 = Joint("elbowIncline", 3, 0, [-1.1, 1.3, 0.2], [0.08, 0.0001, 0, [0,0]])
    joint4 = Joint("elbowRotation", 4, 0, [-1.994, 1.994, 0.2], [0., 0, 0, [0,0]])
    joint5 = Joint("wristIncline", 5, 0, [-1.7, 0.9, 0.2], [0.1, 0.0002, 0, [0,0]])
    joint6 = Joint("wristRotation", 6, 0, [-2.431, 2.431, 0.2], [0.17, 0.0002, 0, [0,0]])

    robotsJoints = [joint1, joint2, joint3, joint4, joint5, joint6]

    # Movement variables
    cmd = [0., 0., 0., 0., 0., 0.]
    move = [0., 0., 0., 0., 0., 0.]

    t = time.time()
    start = t
    t_next = 0
    
    while (True):
        # Sending robot position to the data traitment program
        msgRobot = prepareDatas("Robot", robot.get_joints())
        # msgRobot = prepareDatas("Robot", [0., 0., 0., 0., 0., 0., 0.])    # Used to test when robot is unavailable
        try:
            interprogramComm.send(bytes(msgRobot, "utf-8"))
        except:
            print(">>> Error while sending data")
            break

        # Receiving command from the data traitment program
        try:
            ready = select.select([interprogramComm], [], [], 0.01)
            if ready[0]:
                msgAI = interprogramComm.recv(1024).decode("utf-8")
                datas = dataTraitment(msgAI)
                if datas[0] == "AI":
                    cmd = datas[1]
        except:
            print(">>> Error while receiving the command")
            break
        
        # Make command secure
        cmd = securiseCommand(robotsJoints, cmd)
        
        # Getting robot joints angles
        values = robot.get_joints()

        t_next = time.time()
        dt = t_next - t

        for i in range(6):
            move[i] = robotsJoints[i].PID.calcul(cmd[i], values[i], dt)

        robot.jog_joints(move)

        t = t_next

    if interprogramComm != None:
        print(">>> Closing connection to data traitment program\n")
        interprogramComm.close()

    print("#######################################")
    print("#        Robot control stopped        #")
    print("#######################################")
