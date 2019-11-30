import tkinter as tk
from sys import path
path.append(".\src")

def controlsMenu():
    with open(r".\src\txt_files\controls.txt", "r") as CF:
        string = CF.read()
        CTRLSRoot = tk.Tk()

        mainL = tk.Label(CTRLSRoot, text=string, font=("Consolas", 13))
        mainL.pack()

        CTRLSRoot.mainloop()

def infoMenu():
    with open(r".\src\txt_files/info.txt", "r") as IF:
        string = IF.read()
        IFRoot = tk.Tk()

        mainL = tk.Label(IFRoot, text=string, font=("Consolas", 13))
        mainL.pack()
        IFRoot.mainloop()

class Menu:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Main Menu")
        self.root.iconbitmap(r".\src\ico_files\Main_Menu_ICO.ico")

        self.winHeight = tk.IntVar()
        self.winHeight.set(1080)

        self.winHeightE = tk.Entry()
        self.winHeightE.insert(0, self.winHeight.get())

        self.winWidth = tk.IntVar()
        self.winWidth.set(1920)

        self.winWidthE = tk.Entry()
        self.winWidthE.insert(0, self.winWidth.get())

        self.picHeight = tk.IntVar()
        self.picHeight.set(43)

        self.picHeightE = tk.Entry()
        self.picHeightE.insert(0, self.picHeight.get())

        self.picWidth = tk.IntVar()
        self.picWidth.set(97)

        self.picWidthE = tk.Entry()
        self.picWidthE.insert(0, self.picWidth.get())

    def RUNFEATURELESS(self):
        self.winHeight = self.winHeight.get()
        self.winWidth = self.winWidth.get()

        self.picWidth = self.picWidthE.get()
        self.picHeight = self.picHeightE.get()
        self.root.destroy()

        import Featureless
        Featureless.main(self.winWidth, self.winHeight, self.picHeight, self.picWidth)

    def done(self):
        self.winHeight = self.winHeight.get()
        self.winWidth = self.winWidth.get()

        self.picWidth = self.picWidthE.get()
        self.picHeight = self.picHeightE.get()

        self.root.destroy()
        import Main
        Main.mainInit(self.winWidth, self.winHeight, self.picHeight, self.picWidth)

    def setSetting(self):
        self.winHeight.set(self.winHeightE.get())
        self.winWidth.set(self.winWidthE.get())
        self.picHeight.set(self.picHeightE.get())
        self.picWidth.set(self.picWidthE.get())

        self.root.after(500, self.setSetting)

    def mainMenu(self):

        tk.Label(text="Window height", font=("MS Reference Sans Serif", 15)).grid(column=1, row=1)
        self.winHeightE.grid(column=1, row=2)

        tk.Label(text="Window width", font=("MS Reference Sans Serif", 15)).grid(column=1, row=3)
        self.winWidthE.grid(column=1, row=4)

        tk.Label(text="picture width\n(recommended 97)", font=("MS Reference Sans Serif", 10)).grid(column=2, row=1)
        self.picWidthE.grid(column=2, row=2)

        tk.Label(text="picture height\n(recommended 43)", font=("MS Reference Sans Serif", 10)).grid(column=2, row=3)
        self.picHeightE.grid(column=2, row=4)

        tk.Button(self.root, command=lambda: self.done(), text="run main version", font=("arial", 15), bg="#e1f40c").grid(column=3, row=5)
        tk.Button(self.root, text="run featureless version", font=("arial", 15), command=lambda: self.RUNFEATURELESS(), bg="#f40ce1").grid(column=1, row=5)

        tk.Button(text="Controls", font=("MS Reference Sans Serif", 12), command=lambda: controlsMenu(), bg="#0055ee").grid(column=3, row=1)
        tk.Button(text="Info", font=("MS Reference Sans Serif", 12), command=lambda: infoMenu(), bg="#0055ee").grid(column=3, row=3)

        self.root.update_idletasks()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split("+")[0].split("x"))
        x, y = w / 2 - size[0] / 2, h / 2 - size[1] / 2
        self.root.geometry("%dx%d+%d+%d" %(size + (x, y)))
        self.setSetting()

        self.root.mainloop()
if __name__ == '__main__':
    Menu().mainMenu()