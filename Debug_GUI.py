# Project 14 : Controling a robotic arm using VR
# Modification date : 14/03/2023 - Tanguy
# File : GUI to watch the commands and the respond from the robot

# Importing needed librairies
from tkinter import *
from PIL import ImageTk, Image
import sys, socket, time, select
from pyniryo import *
from Data_traitment import dataTraitment
from display_functions import print_ascii_art

print_ascii_art("DispLogo.png", 10, 0.01)

print("#######################################")
print("#           GUI has awakend           #")
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
    print("#        GUI returns to ashes         #")
    print("#######################################")
    sys.exit()

# Update time of the frame
updateTime = 20
error = 0

# GUI parameters
background = "#333333"
foreground = "#FFFFFF"

# List the asked position and the robot's position
SendPos = [0.,0.,0.,0.,0.,0.]
RobotPos = [0.,0.,0.,0.,0.,0.]

window = Tk()
window.geometry("720x720")
window.resizable(False, False)
window.title("BraVeD Control Center")
window.config(bg=background)

mainFrame = Frame(window, bg=background)
mainFrame.pack(side=RIGHT, padx=60)

imgWidth, imgHeight = 300, 300
cnv = Canvas(window, width=imgWidth, height=imgHeight, bg=background, bd=0, highlightthickness=0)
img = Image.open("LogoBraVeD.png").resize((imgWidth, imgHeight), Image.ANTIALIAS)
cnv.image = ImageTk.PhotoImage(img)
cnv.create_image(imgWidth/2, imgHeight/2, image=cnv.image)
cnv.place(x=10, y=210)

mainFrame = Frame(window, bg=background)
mainFrame.pack(side=RIGHT, padx=60)

AI_Frame = Frame(mainFrame, bg=background)
AI_Frame.grid(row=0, column=1)

Action_Frame = Frame(mainFrame, bg=background)
Action_Frame.grid(row=2, column=1, pady=15)

RobotFrame = Frame(mainFrame, bg=background)
RobotFrame.grid(row=1, column=1)

def stopp():
    if interprogramComm != None:
        print(">>> Closing connection to data traitment program\n")
        interprogramComm.close()

    print("#######################################")
    print("#        GUI returns to ashes         #")
    print("#######################################")
    sys.exit()

Button(Action_Frame, text="Stop", fg="#FFFFFF", bg="#FF0000", font=("Arial", 20), command=stopp).pack(side=RIGHT)

def destroyChildA(element):
    for child in element.winfo_children():
        child.destroy()

def packInfos(texte):
    global SendPos, RobotPos
    if (texte == "AI"):
        destroyChildA(AI_Frame)
        Label(AI_Frame, text="AI", fg=foreground, bg=background, font=("Arial", 24, "bold")).grid(row=0, column=0)
        textSendPos = f"Q1 = {round(SendPos[0], 2)}\nQ2 = {round(SendPos[1], 2)}\nQ3 = {round(SendPos[2], 2)}\nQ4 = {round(SendPos[3], 2)}\nQ5 = {round(SendPos[4], 2)}\nQ6 = {round(SendPos[5], 2)}"
        Label(AI_Frame, text=textSendPos, fg=foreground, bg=background, font=("Arial", 20)).grid(row=1, column=0, pady=15)
    if (texte == "Robot"):
        destroyChildA(RobotFrame)
        Label(RobotFrame, text="Robot's\nposition", fg=foreground, bg=background, font=("Arial", 24, "bold")).grid(row=0, column=0, pady=15)
        textRobotPos = f"Q1 = {round(RobotPos[0], 2)}\nQ2 = {round(RobotPos[1], 2)}\nQ3 = {round(RobotPos[2], 2)}\nQ4 = {round(RobotPos[3], 2)}\nQ5 = {round(RobotPos[4], 2)}\nQ6 = {round(RobotPos[5], 2)}"
        Label(RobotFrame, text=textRobotPos, fg=foreground, bg=background, font=("Arial", 20)).grid(row=1, column=0)

def receiveData():
    global interprogramComm, SendPos, RobotPos, window, error
    ready = select.select([interprogramComm], [], [], 0.01)
    if ready[0]:
        msg = interprogramComm.recv(1024).decode("utf-8")
        datas = dataTraitment(msg)
        if datas[0] != -1:
            error = 0
            if datas[0] == "AI":
                SendPos = datas[1]
            if datas[0] == "Robot":
                RobotPos = datas[1]
            packInfos(datas[0])
            time.sleep(1/updateTime)
        else:
            error += 1
    if error > 10:
        print(">>> No response from the data traitment program")
        stopp()
    window.after(updateTime, receiveData)

window.after(updateTime, receiveData)
window.mainloop()