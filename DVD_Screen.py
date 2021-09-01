import tkinter as tk
import pygame
import random
import os
import json
import playsound
import importlib

def _Main():
    from src.Main import main
    print("Loading... 50%")
    main(Menu.winWidth, Menu.winHeight, Menu.picHeight, Menu.picWidth)


def controlsMenu():
    with open(r"./src/txt_files/controls.txt", "r") as CF:
        CTRLSRoot = tk.Tk()

        mainL = tk.Label(CTRLSRoot, text=CF.read(), font=("Consolas", 13))
        mainL.pack()

        CTRLSRoot.mainloop()

def infoMenu():
    with open(r"./src/txt_files/info.txt", "r") as IF:
        IFRoot = tk.Tk()

        mainL = tk.Label(IFRoot, text=IF.read(), font=("Consolas", 13))
        mainL.pack()

        IFRoot.mainloop() 

class Menu(tk.Tk):
    with open(r"src/buttonColors.json") as colorsJson:
        data = json.load(colorsJson)
        BGColor = data["backgroundColor"]
        otherButtons = data["otherButtons"]
        mainBs = data["mainButtons"]
        quitButton = data["quitButton"]
    with open("DEFAULTS.json", "r") as RF: #gets the default width, height from the DEFAULTS.json file
        data = json.load(RF)
        winWidth = data["screen"]["width"]
        winHeight = data["screen"]["height"]
        picWidth = data["images"]["width"]
        picHeight = data["images"]["height"]
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.configure(background=Menu.BGColor)

        self.title(random.choice(["DVD Screen", "Main Menu", "Cool Title Here", "I'm Surprised You Read This", "New And Improved"]))
        
        self.winHeightE = tk.Entry()
        self.winHeightE.insert(0, Menu.winHeight)
        
        self.winWidthE = tk.Entry()
        self.winWidthE.insert(0, Menu.winWidth)

        self.picHeightE = tk.Entry()
        self.picHeightE.insert(0, Menu.picHeight)

        self.picWidthE = tk.Entry()
        self.picWidthE.insert(0, Menu.picWidth)

        self.bind("<F10>", lambda x: self.done("secret"))

    def done(self, version): #runs the picked version6

        Menu.winHeight, Menu.winWidth = int(self.winHeightE.get()), int(self.winWidthE.get())

        Menu.picWidth, Menu.picHeight = int(self.picWidthE.get()), int(self.picHeightE.get())

        self.destroy()

        print("Loading...")
        if version == "main":
            _Main()

        elif version == "featureless":
            import src.Featureless as Featureless
            print("Loading... 50%")
            Featureless.main(Menu.winWidth, Menu.winHeight, Menu.picHeight, Menu.picWidth)

        elif version == "secret":
            import src.Secret as Secret
            Secret.main(random.randint(15, 25), Menu.picHeight, Menu.picWidth, Menu.winWidth, Menu.winHeight) 

    def mainMenu(self):                    

        tk.Label(text="Window width", font=("MS Reference Sans Serif", 15), bg=Menu.BGColor).grid(column=1, row=3)
        self.winHeightE.grid(column=1, row=2)

        tk.Label(text="Window height", font=("MS Reference Sans Serif", 15), bg=Menu.BGColor).grid(column=1, row=1)
        self.winWidthE.grid(column=1, row=4)

        tk.Label(text="picture width\n(recommended 97)", font=("MS Reference Sans Serif", 10), bg=Menu.BGColor).grid(column=2, row=1)
        self.picWidthE.grid(column=2, row=2)

        tk.Label(text="picture height\n(recommended 43)", font=("MS Reference Sans Serif", 10), bg=Menu.BGColor).grid(column=2, row=3)
        self.picHeightE.grid(column=2, row=4)

        #main version
        tk.Button(self, command=lambda: self.done("main"), text="run main version", font=(Menu.mainBs["font"], 15), bg=Menu.mainBs["color"]).grid(column=3, row=6)
        #featureless version
        tk.Button(self, text="run featureless version", font=(Menu.mainBs["font"], 15), command=lambda: self.done("featureless"), bg=Menu.mainBs["color"]).grid(column=1, row=6)

		#other buttons
        tk.Button(text="Controls", font=(Menu.otherButtons["font"], 12), command=lambda: controlsMenu(), bg=Menu.otherButtons["color"]).grid(column=3, row=1)
        tk.Button(text="Info", font=(Menu.otherButtons["font"], 12), command=lambda: infoMenu(), bg=Menu.otherButtons["color"], width=13).grid(column=4, row=6)
        tk.Button(text="Open Defaults", font=(Menu.otherButtons["font"], 12), command=lambda: os.system(r".\DEFAULTS.json"), bg=Menu.otherButtons["color"]).grid(column=3, row=3)
        tk.Button(text="Open Logos foler", font=(Menu.otherButtons["font"], 12), command=lambda: os.startfile("DVD_Logos"), bg=Menu.otherButtons["color"]).grid(column=4, row=3)
        tk.Button(text="Open Screenshots folder", font=(Menu.otherButtons["font"], 12), command=lambda: os.startfile("SCREENSHOTS"), bg=Menu.otherButtons["color"]).grid(column=4, row=1)

        #QUIT button
        tk.Button(text="   QUIT   ", font=(Menu.quitButton["font"], 12), command=lambda: self.destroy(), bg=Menu.quitButton["color"]).grid(column=2, row=6)
        self.update_idletasks()
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split("+")[0].split("x"))
        x, y = w / 2 - size[0] / 2, h / 2 - size[1] / 2
        self.geometry("%dx%d+%d+%d" %(size + (x, y)))
        self.mainloop()

if __name__ == '__main__': Menu().mainMenu()
