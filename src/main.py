import tkinter as tk
from tkinter import ttk
import sv_ttk
from PIL import Image, ImageTk
from pathlib import Path
import os


class MainGUI:
    def __init__(self, mainWindow):
        self.assets_dir = Path(__file__).parent.parent / "assets"
        self.logo_dir = os.path.join(self.assets_dir, "Rexair-LLC.png")
        
        mainWindow.title("Rexair Automation Controller")
        self.mainWindowWidth = mainWindow.winfo_screenwidth()
        self.mainWindowHeight = mainWindow.winfo_screenheight()
        mainWindow.geometry(f"{self.mainWindowWidth}x{self.mainWindowHeight}+0+0")
        self.image = Image.open(self.logo_dir)
        self.image = self.image.resize((int(self.mainWindowWidth/4), int(self.mainWindowHeight/4)))
        self.image = ImageTk.PhotoImage(self.image)
        self.bg_label = tk.Label(mainWindow, image = self.image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.image = self.image

        self.scanResultsPane = tk.Frame(mainWindow, width=int(self.mainWindowWidth/4), height=int(self.mainWindowHeight*0.9))
        self.scanResultsPane.pack_propagate(False)
        self.scanResultsPane.pack(side='left', anchor="w")
        self.canvases = []
        for i in range(7):
            canvas = tk.Canvas(self.scanResultsPane, relief='raised', borderwidth=2, width=int(self.mainWindowWidth/4), height=int(self.mainWindowHeight*0.075), bg="white")
            canvas.pack()
            self.canvases.append(canvas)

        sv_ttk.set_theme("light")

    def listDevices(self, frame):
        values = ["Option 1", "Option 2", "Option 3"]
        combobox1 = ttk.Combobox(self.scanResultsPane, values=values)
        combobox1.grid(row=0, column=0)
        # combobox1.pack()
        combobox2 = ttk.Combobox(self.scanResultsPane, values=values)
        combobox2.grid(row=1, column=0)
        # combobox2.pack()

    def drawTOF(self, mainWindow, index):
        offset = 10
        self.rect = {}
        self.oval = {}
        self.cellwidth = 10
        self.cellheight = 10
        for column in range(4):
            for row in range(4):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                x1 += offset
                x2 += offset
                y1 += offset
                y2 += offset
                self.rect[row,column] = self.canvases[index].create_rectangle(x1,y1,x2,y2, fill="blue", tags="rect")
                self.oval[row,column] = self.canvases[index].create_oval(x1+2,y1+2,x2-2,y2-2, fill="gray", tags="oval")

        
 

def main():
    root = tk.Tk()
    GUI = MainGUI(root)
    for val in range(7):
        GUI.drawTOF(root, val)
    root.mainloop()


if __name__=="__main__":
    main()