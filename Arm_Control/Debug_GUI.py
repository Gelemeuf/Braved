# Projet 14 : Contrôle d'un bras robot à l'aide d'un casque de VR
# Date de modification : 18/11/2022 - Tanguy

# Importation des librairies nécessaires
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import time
from pyniryo import *


class robotGUI:

    window = None
    title = None
    connectionFrame = None
    connectButton = None
    background = "#313131"
    foreground = "#FFFFFF"

    def __init__(self) -> None:
        self.window = Tk()
        self.window.geometry("1280x720")
        self.window.resizable(False, False)
        self.window.title("Control GUI")
        self.window.config(bg=self.background)
        pass

    def packImage(self, image, width, height, posX, posY, command=None, element=None) -> None:
        if (element == None):
            cnv = Canvas(self.window, width=width, height=height, bg=self.background, bd=0, highlightthickness=0)
        else:
            cnv = Canvas(element, width=width, height=height, bg=self.background, bd=0, highlightthickness=0)
        img = Image.open(image).resize((width, height), Image.ANTIALIAS)
        cnv.image = ImageTk.PhotoImage(img)
        cnv.create_image(width/2, height/2, image=cnv.image)
        cnv.place(x=posX, y=posY)
        if (command != None):
            cnv.bind('<Button-1>', command)
        return cnv

    def packText(self, text, font, posX, posY, command=None) -> None:
        Text = Label(self.window, text=text, font=font, fg=self.foreground, bg=self.background)
        Text.place(x=posX, y=posY)
        if command != None:
            Text.bind('<Button-1>', command)
        return Text

    def interfaceMenu(self) -> None:
        self.packImage("LogoBraVeD.png", 200, 200, 540, 0)

        AI_Frame = Frame(self.window, bg=self.background)
        AI_Frame.pack(side=LEFT)

        Button(self.window, text="Connect", fg="#FFFFFF", bg="green", font=("Arial", 20)).place(x=580, y=360)

        RobotFrame = Frame(self.window, bg=self.background)
        RobotFrame.pack(side=RIGHT)

        Label(AI_Frame, text="AI", fg=self.foreground, bg=self.background, font=("Arial", 40, "bold")).grid(row=0, column=0)
        SendPos = [0.,0.,0.,0.,0.,0.]
        textSendPos = f"x={SendPos[0]}\ny={SendPos[1]}\nz={SendPos[2]}\nroll={SendPos[3]}\npitch={SendPos[4]}\nyaw={SendPos[5]}"
        Label(AI_Frame, text=textSendPos, fg=self.foreground, bg=self.background, font=("Arial", 20)).grid(row=1, column=0)

        Label(RobotFrame, text="Robot's position", fg=self.foreground, bg=self.background, font=("Arial", 40, "bold")).grid(row=0, column=0)
        RobotPos = [0.,0.,0.,0.,0.,0.]
        textRobotPos = f"x={RobotPos[0]}\ny={RobotPos[1]}\nz={RobotPos[2]}\nroll={RobotPos[3]}\npitch={RobotPos[4]}\nyaw={RobotPos[5]}"
        Label(RobotFrame, text=textRobotPos, fg=self.foreground, bg=self.background, font=("Arial", 20)).grid(row=1, column=0)
        pass

if __name__ == "__main__":
    App = robotGUI()

    def connect(Button):
        for child in App.window.winfo_children():
            child.destroy()
        App.interfaceMenu()

    App.packImage("LogoBraVeD.png", 400, 400, 440, 160, connect)

    App.window.mainloop()