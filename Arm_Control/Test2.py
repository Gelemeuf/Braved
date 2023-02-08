from pyniryo import *
from simple_pid import PID
import time

robotAddress_Ethernet = "169.254.200.200"

robot = NiryoRobot(robotAddress_Ethernet)
    
robot.calibrate_auto()
robot.move_to_home_pose()

pid = PID(0.03, 0, 0, setpoint=2.6)

pid.sample_time = 0.025

v = robot.get_joints()[0]

"""while True:
    t = time.time()
    control = pid(v)
    if control > 0.4:
        control = 0.1
    robot.jog_joints(control, 0, 0, 0, 0, 0)
    v = robot.get_joints()[0]
    if abs(v) > 2.4:
        pid.setpoint = -(pid.setpoint)
    print(time.time()-t)"""
t = time.time()
robot.pos = 0.2,0,0.2,0,0,0
print(time.time()-t)