import tkinter as tk
from tkinter import ttk
import sv_ttk
from PIL import Image, ImageTk
from pathlib import Path
import os
from rexserial import serialPolling
import asyncio


class MainGUI:
    def __init__(self, mainWindow):
        self.assets_dir = Path(__file__).parent.parent / "assets"
        self.logo_dir = os.path.join(self.assets_dir, "Rexair-LLC.png")
        self.scanRequested = False
        self.stationCount = 0
        self.canvases = []

        mainWindow.title("Rexair Automation Controller")
        self.mainWindowWidth = mainWindow.winfo_screenwidth()
        self.mainWindowHeight = mainWindow.winfo_screenheight()
        mainWindow.geometry(f"{self.mainWindowWidth}x{self.mainWindowHeight}+0+0")

        self.scanResultsPane = tk.Frame(
            mainWindow,
            width=int(self.mainWindowWidth / 4),
            height=int(self.mainWindowHeight * 0.9),
        )
        self.scanResultsPane.pack_propagate(False)
        self.scanResultsPane.pack(side="left", anchor="w")

        self.controlPanel = tk.Frame(
            mainWindow,
            width=int(self.mainWindowWidth / 4),
            height=int(self.mainWindowHeight * 0.9),
        )
        self.controlPanel.pack_propagate(False)
        self.controlPanel.pack(side="left", anchor="w")

        self.scanButton = tk.Button(
            self.controlPanel, text="Scan", command=self.drawScan
        )
        self.scanButton.config(height=3, width=10)
        self.scanButton.pack(side="top")
        self.clearButton = tk.Button(
            self.controlPanel, text="Clear", command=self.clearScan
        )
        self.clearButton.config(height=3, width=10)
        self.clearButton.pack(side="top")

        self.logoPane = tk.Frame(
            mainWindow,
            width=int(self.mainWindowWidth / 4),
            height=int(self.mainWindowHeight * 0.9),
        )
        self.logoPane.pack_propagate(False)
        self.logoPane.pack(side="right", anchor="e")
        self.image = Image.open(self.logo_dir)
        self.image = self.image.resize(
            (int(self.mainWindowWidth / 10), int(self.mainWindowHeight / 10))
        )
        self.image = ImageTk.PhotoImage(self.image)
        self.bg_label = tk.Label(self.logoPane, image=self.image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.image = self.image
        self.bg_label.pack(side="bottom")

        sv_ttk.set_theme("light")

    def setlocalCOM(self, comHandle):
        self.comPort = comHandle

    def drawStations(self):
        self.stationCount += 1
        canvas = tk.Canvas(
            self.scanResultsPane,
            relief="raised",
            borderwidth=2,
            width=int(self.mainWindowWidth / 4),
            height=int(self.mainWindowHeight * 0.075),
            bg="white",
        )
        canvas.pack()
        self.canvases.append(canvas)

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
                x1 = column * self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                x1 += offset
                x2 += offset
                y1 += offset
                y2 += offset
                if index == 4:
                    color = "#90EE90"
                else:
                    color = "white"

                self.rect[row, column] = self.canvases[index].create_rectangle(
                    x1, y1, x2, y2, fill=color, tags="rect"
                )
                self.oval[row, column] = self.canvases[index].create_oval(
                    x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill="gray", tags="oval"
                )
        xpos = self.canvases[index].winfo_width() - 10
        ypos = 50
        self.canvases[index].create_text(
            xpos, ypos, anchor="e", text=f"Station {index+1}", font=("Arial", 16)
        )

    def drawScan(self):
        self.scanRequested = True

    def clearScan(self):
        for i in range(0, self.stationCount):
            self.canvases[i].destroy()

        self.canvases = []
        self.stationCount = 0

    def saveValues(self, rootVal, GUIVal):
        self.root = rootVal
        self.GUI = GUIVal


async def main():
    root = tk.Tk()
    GUI = MainGUI(root)
    comPort = serialPolling("/dev/ttyS1", 115200, 1)
    GUI.setlocalCOM(comPort)
    GUI.saveValues(root, GUI)

    while True:
        root.update_idletasks()
        root.update()
        # if scan requested
        if GUI.scanRequested == True:
            GUI.scanRequested = False
            for j in range(1, 8):
                value_encoded = bytearray(
                    [0xA5, 0x08, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00]
                )
                value_encoded[2] = j
                value = comPort.PktEncode(value_encoded)
                await comPort.pollWriteController(value)
                await asyncio.sleep(0.2)
                result = await comPort.pollReadController()
                returnValue = comPort.PktDecode(result)
                print(bytes(returnValue))
                GUI.drawStations()
                root.update()

        value_encoded = bytearray([0xA5, 0x08, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00])
        value = comPort.PktEncode(value_encoded)
        # await comPort.pollWriteController(value)
        await asyncio.sleep(0.2)
        # result = await comPort.pollReadController()


if __name__ == "__main__":
    asyncio.run(main())
