import tkinter as tk
from os import environ
class Menu:
    def __init__(self):
        self.root = tk.Tk()

        self.winHeight = tk.IntVar()
        self.winHeight.set(1080)

        self.winHeightE = tk.Entry()
        self.winHeightE.insert(0, self.winHeight.get())

        self.winWidth = tk.IntVar()
        self.winWidth.set(1920)

        self.winWidthE = tk.Entry()
        self.winWidthE.insert(0, self.winWidth.get())

    def controlsMenu(self):
        with open("controls.txt", "r") as CF:
            string = CF.read()
            CTRLSRoot = tk.Tk()

            mainL = tk.Label(CTRLSRoot, text=string, font=("Consolas", 13))
            mainL.pack()

            environ['SDL_VIDEO_CENTERED'] = "1"
            CTRLSRoot.mainloop()

    def infoMenu(self):
        with open("info.txt", "r") as IF:
            string = IF.read()
            IFRoot = tk.Tk()

            mainL = tk.Label(IFRoot, text=string, font=("Consolas", 13))
            mainL.pack()
            environ['SDL_VIDOE_CENTERED'] = "1"
            IFRoot.mainloop()
        

    def done(self):
        self.winHeight = self.winHeight.get()
        self.winWidth = self.winWidth.get()

        self.root.destroy()

    def setSetting(self):
        self.winHeight.set(self.winHeightE.get())
        self.winWidth.set(self.winWidthE.get())

        print(self.winHeight.get())

        self.root.after(500, self.setSetting)

    def mainMenu(self):
        environ['SDL_VIDEO_CENTERED'] = "1"

        tk.Label(text="Window height", font=("MS Reference Sans Serif", 23)).pack()

        self.winHeightE.pack()

        tk.Label(text="Window width", font=("MS Reference Sans Serif", 23)).pack()

        
        self.winWidthE.pack()

        doneB = tk.Button(self.root, command=lambda: self.done(), text="done", font=("Valken", 20))
        doneB.pack()

        controlsB = tk.Button(text="Controls", font=("MS Reference Sans Serif", 10), command=lambda: self.controlsMenu())
        controlsB.pack()

        infoB = tk.Button(text="Info", font=("MS Reference Sans Serif", 10), command=lambda: self.infoMenu())
        infoB.pack()

        self.setSetting()

        self.root.mainloop()
