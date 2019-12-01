import tkinter as tk
from sys import path
import random
path.append(".\src")

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

class Menu:
    def __init__(self):
        self.root = tk.Tk()

        self.root.configure(background="#ffffff")

        self.root.title(random.choice(["DVD Screen", "Main Menu", "Cool Title Here", "I'm Surprised You Read This", "New And Improved"]))
        self.root.iconbitmap(r".\src\ico_files\Main_Menu_ICO.ico")
        
        self.winHeightE = tk.Entry()
        self.winHeightE.insert(0, 1080)
        
        self.winWidthE = tk.Entry()
        self.winWidthE.insert(0, 1920)

        self.picHeightE = tk.Entry()
        self.picHeightE.insert(0, 43)

        self.picWidthE = tk.Entry()
        self.picWidthE.insert(0, 97)

    def RUNFEATURELESS(self): #featureless
        winHeight, winWidth = int(self.winHeightE.get()), int(self.winWidthE.get())
        picWidth, picHeight = int(self.picWidthE.get()), int(self.picHeightE.get())

        self.root.destroy()

        print("Loading...")
        from Featureless import main
        print("Loading... 50%")
        main(winWidth, winHeight, picHeight, picWidth)

    def done(self): #main
        winHeight, winWidth = int(self.winHeightE.get()), int(self.winWidthE.get())

        picWidth, picHeight = int(self.picWidthE.get()), int(self.picHeightE.get())

        self.root.destroy()

        print("Loading...")
        from Main import mainInit
        print("Loading... 50%")
        mainInit(winWidth, winHeight, picHeight, picWidth)

    def mainMenu(self):

        tk.Label(text="Window height", font=("MS Reference Sans Serif", 15), bg="#ffffff").grid(column=1, row=1)
        self.winHeightE.grid(column=1, row=2)

        tk.Label(text="Window width", font=("MS Reference Sans Serif", 15), bg="#ffffff").grid(column=1, row=3)
        self.winWidthE.grid(column=1, row=4)

        tk.Label(text="picture width\n(recommended 97)", font=("MS Reference Sans Serif", 10), bg="#ffffff").grid(column=2, row=1)
        self.picWidthE.grid(column=2, row=2)

        tk.Label(text="picture height\n(recommended 43)", font=("MS Reference Sans Serif", 10), bg="#ffffff").grid(column=2, row=3)
        self.picHeightE.grid(column=2, row=4)

        tk.Button(self.root, command=lambda: self.done(), text="run main version", font=("arial", 15), bg="#1cdb15").grid(column=3, row=5)
        tk.Button(self.root, text="run featureless version", font=("arial", 15), command=lambda: self.RUNFEATURELESS(), bg="#1cdb15").grid(column=1, row=5)

        tk.Button(text="Controls", font=("MS Reference Sans Serif", 12), command=lambda: controlsMenu(), bg="#0055ee").grid(column=3, row=1)
        tk.Button(text="Info", font=("MS Reference Sans Serif", 12), command=lambda: infoMenu(), bg="#0055ee").grid(column=3, row=3)

        self.root.update_idletasks()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split("+")[0].split("x"))
        x, y = w / 2 - size[0] / 2, h / 2 - size[1] / 2
        self.root.geometry("%dx%d+%d+%d" %(size + (x, y)))

        self.root.mainloop()
if __name__ == '__main__':
    Menu().mainMenu()