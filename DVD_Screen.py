import tkinter as tk
import pygame
from sys import path
import random
import os

path.append(".\src")

def _Main():
    import Main
    print("Loading... 50%")
    Main.mainInit(Menu.winWidth, Menu.winHeight, Menu.picHeight, Menu.picWidth)

def controlsMenu():
    with open(r".\src\txt_files\controls.txt", "r") as CF:
        CTRLSRoot = tk.Tk()

        mainL = tk.Label(CTRLSRoot, text=CF.read(), font=("Consolas", 13))
        mainL.pack()

        CTRLSRoot.mainloop()

def infoMenu():
    with open(r".\src\txt_files/info.txt", "r") as IF:
        IFRoot = tk.Tk()

        mainL = tk.Label(IFRoot, text=IF.read(), font=("Consolas", 13))
        mainL.pack()

        IFRoot.mainloop()

def defaultsMenu():
    os.system(".\DEFAULTS.txt")

class Menu:
    BGColor = "#eeeeee"
    otherBColor = "#e324ea"
    with open("DEFAULTS.txt", "r") as RF: #gets the default width, height from the DEFAULTS.txt file
        text = (RF.read()).split(" ")
        winWidth, winHeight = text[1], text[2]
        picWidth, picHeight = text[4], text[5]
    def __init__(self):
        self.root = tk.Tk()

        self.root.configure(background=Menu.BGColor)

        self.root.title(random.choice(["DVD Screen", "Main Menu", "Cool Title Here", "I'm Surprised You Read This", "New And Improved"]))
        self.root.iconbitmap(r".\src\ico_files\Main_Menu_ICO.ico")
        
        self.winHeightE = tk.Entry()
        self.winHeightE.insert(0, Menu.winHeight)
        
        self.winWidthE = tk.Entry()
        self.winWidthE.insert(0, Menu.winWidth)

        self.picHeightE = tk.Entry()
        self.picHeightE.insert(0, Menu.picHeight)

        self.picWidthE = tk.Entry()
        self.picWidthE.insert(0, Menu.picWidth)

        self.root.bind("<F10>", lambda x: self.done("secret"))

    def done(self, version): #runs the picked version6

        Menu.winHeight, Menu.winWidth = int(self.winHeightE.get()), int(self.winWidthE.get())

        Menu.picWidth, Menu.picHeight = int(self.picWidthE.get()), int(self.picHeightE.get())

        self.root.destroy()

        print("Loading...")
        if version == "main":
            _Main()

        elif version == "featureless":
            import Featureless
            print("Loading... 50%")
            Featureless.main(Menu.winWidth, Menu.winHeight, Menu.picHeight, Menu.picWidth)

        elif version == "secret":
            import Secret
            Secret.main(random.randint(15, 25), Menu.picHeight, Menu.picWidth, Menu.winWidth, Menu.winHeight)

    def xButton(self):
        self.root.destroy() 
        return


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
        tk.Button(self.root, command=lambda: self.done("main"), text="run main version", font=("arial", 15), bg="#1cdb15").grid(column=3, row=6)
        #featureless version
        tk.Button(self.root, text="run featureless version", font=("arial", 15), command=lambda: self.done("featureless"), bg="#1cdb15").grid(column=1, row=6)

		#other buttons
        tk.Button(text="Controls", font=("MS Reference Sans Serif", 12), command=lambda: controlsMenu(), bg=Menu.otherBColor).grid(column=3, row=1)
        tk.Button(text="Info", font=("MS Reference Sans Serif", 12), command=lambda: infoMenu(), bg=Menu.otherBColor).grid(column=3, row=2)
        tk.Button(text="Open Defaults", font=("MS Reference Sans Serif", 12), command=lambda: defaultsMenu(), bg=Menu.otherBColor).grid(column=3, row=3)

        #QUIT button
        tk.Button(text="QUIT", font=("MS Reference Sans Serif", 12), command=lambda: self.root.destroy(), bg="#d81111").grid(column=2, row=6)

        self.root.update_idletasks()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split("+")[0].split("x"))
        x, y = w / 2 - size[0] / 2, h / 2 - size[1] / 2
        self.root.geometry("%dx%d+%d+%d" %(size + (x, y)))
        self.root.protocol("WM_DELETE_WINDOW", self.xButton)
        self.root.mainloop()


if __name__ == '__main__': Menu().mainMenu()