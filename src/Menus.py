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

        self.picHeight = tk.IntVar()
        self.picHeight.set(97)

        self.picHeightE = tk.Entry()
        self.picHeightE.insert(0, self.picHeight.get())

        self.picWidth = tk.IntVar()
        self.picWidth.set(43)

        self.picWidthE = tk.Entry()
        self.picWidthE.insert(0, self.picWidth.get())

    def RUNFEATURELESS(self):
        self.root.destroy()
        import Featureless

    def controlsMenu(self):
        with open(r".\src\txt_files\controls.txt", "r") as CF:
            string = CF.read()
            CTRLSRoot = tk.Tk()

            mainL = tk.Label(CTRLSRoot, text=string, font=("Consolas", 13))
            mainL.pack()

            environ['SDL_VIDEO_CENTERED'] = "1"
            CTRLSRoot.mainloop()

    def infoMenu(self):
        with open(r".\src\txt_files/info.txt", "r") as IF:
            string = IF.read()
            IFRoot = tk.Tk()

            mainL = tk.Label(IFRoot, text=string, font=("Consolas", 13))
            mainL.pack()
            environ['SDL_VIDOE_CENTERED'] = "1"
            IFRoot.mainloop()
        

    def done(self):
        self.winHeight = self.winHeight.get()
        self.winWidth = self.winWidth.get()

        self.picWidth = self.picWidthE.get()
        self.picHeight = self.picHeightE.get()

        self.root.destroy()

    def setSetting(self):
        self.winHeight.set(self.winHeightE.get())
        self.winWidth.set(self.winWidthE.get())
        self.picHeight.set(self.picHeightE.get())
        self.picWidth.set(self.picWidthE.get())

        self.root.after(500, self.setSetting)

    def mainMenu(self):
        environ['SDL_VIDEO_CENTERED'] = "1"

        tk.Label(text="Window height", font=("MS Reference Sans Serif", 15)).grid(column=1, row=1)
        self.winHeightE.grid(column=1, row=2)

        tk.Label(text="Window width", font=("MS Reference Sans Serif", 15)).grid(column=1, row=3)
        self.winWidthE.grid(column=1, row=4)

        tk.Label(text="picture width\nRECOMMENDED DEFAULT", font=("MS Reference Sans Serif", 10)).grid(column=1, row=5)
        self.picWidthE.grid(column=1, row=6)

        tk.Label(text="picture height\nRECOMMENDED DEFAULT", font=("MS Reference Sans Serif", 10)).grid(column=1, row=7)
        self.picHeightE.grid(column=1, row=8)

        doneB = tk.Button(self.root, command=lambda: self.done(), text="run main version", font=("arial", 15))
        doneB.grid(column=3, row=1)
        featureLessB = tk.Button(self.root, text="run featureless ersion", font=("arial", 10), command=lambda: self.RUNFEATURELESS())
        featureLessB.grid(column=3, row=8)

        controlsB = tk.Button(text="Controls", font=("MS Reference Sans Serif", 10), command=lambda: self.controlsMenu())
        controlsB.grid(column=2, row=3)

        infoB = tk.Button(text="Info", font=("MS Reference Sans Serif", 10), command=lambda: self.infoMenu())
        infoB.grid(column=2, row=5)

        self.root.update_idletasks()
        w =self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split("+")[0].split("x"))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        self.root.geometry("%dx%d+%d+%d" %(size + (x, y)))
        self.setSetting()

        self.root.mainloop()
