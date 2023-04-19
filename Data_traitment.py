# Project 14 : Controling a robotic arm using VR
# Modification date : 14/03/2023 - Tanguy
# File : Linking program

# Importing needed librairies
import socket, time
import numpy as np
from display_functions import print_ascii_art

# Used to reduced trafic on the network
WaitTime = 0.01
sharingUnit = 0

# Functions used to prepare data and send them
def dataTraitment(msg):
    value = [0, 0, 0, 0, 0, 0]
    try:
        temp = msg.split(":")
        tmp = temp[1].split(",")[0:6]
        for i in range(6):
            value[i] = float(tmp[i])
        return [temp[0], value]
    except:
        return [-1, [0.,0.,0.,0.,0.,0.]]

def prepareDatas(Comp, values):
    message = Comp+":"
    if len(values) == 6:
        for element in values:
            message += str(element)+","
        return message
    else:
        return -1

# Main program
if __name__ == "__main__":
    print_ascii_art("DispLogo.png", 10, 0.01)
    print("\n")
    print("#######################################")
    print("#   Program interconnection started   #")
    print("#######################################\n")

    AI = [0., 0., 0., 0., 0., 0.]
    Robot = [0., 0., 0., 0., 0., 5.]

    # 
    host, port = ('localhost', 1234)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((host, port))

    # Wait for all the subprogram to connect
    socket.listen(5)
    answer = "0"
    while answer != "Y":
        print("Connect the Camera program")
        CAMconn, CAMaddress = socket.accept()
        print(f">>> Connection with Camera program established at {CAMaddress[0]}\n")
        answer = input("Has the camera program started correctly ? (Y/N) : ")
        print("\n")

    print("Connect the GUI program")
    GUIconn, GUIaddress = socket.accept()
    print(f">>> Connection with GUI program established at {GUIaddress[0]}\n")

    print("Connect the visualisation program")
    VIZconn, VIZaddress = socket.accept()
    print(f">>> Connection with visualisation program established at {VIZaddress[0]}\n")

    print("Connect the robot control program")
    Robconn, Robaddress = socket.accept()
    print(f">>> Connection with robot control program established at {Robaddress[0]}\n")

    while True:
        try:
            # Read data from camera
            try:
                CAMconn.send(b'')
            except:
                print(">>> No answer from Camera program")
                break

            msgAI = CAMconn.recv(1024)
            data = dataTraitment(msgAI.decode("utf-8"))
            if data[0] == "AI":
                AI = data[1]

            # Send to and read from robot control program
            try:
                Robconn.send(b'')
            except:
                print(">>> No answer from robot control program")
                break

            msgRobot = Robconn.recv(1024)
            Robconn.send(msgAI)

            # Send data to GUI
            if sharingUnit:
                GUIconn.send(msgAI)
                VIZconn.send(msgAI)
            else:
                GUIconn.send(msgRobot)
                VIZconn.send(msgRobot)

            sharingUnit = (sharingUnit + 1)%2

            # Reduce trafic on network
            time.sleep(WaitTime)

        except:
            break
    
    print(">>> Connection to one of the program failed")
    print(">>> Closing connection for all\n")
    socket.close()

    print("#######################################")
    print("#   Program interconnection stopped   #")
    print("#######################################")