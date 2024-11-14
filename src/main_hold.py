import tkinter as tk
import os
import asyncio
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
from rexserial import serialPolling


class MainGUI:
    stationCount = 0
    root = 0

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
            highlightbackground="black",
            highlightthickness="1",
        )
        self.scanResultsPane.pack_propagate(False)
        self.scanResultsPane.pack(side="left", anchor="w")

        self.controlPanel = tk.Frame(
            mainWindow,
            width=int(self.mainWindowWidth / 4),
            height=int(self.mainWindowHeight * 0.9),
            highlightbackground="black",
            highlightthickness="1",
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

    def setlocalCOM(self, comHandle):
        self.comPort = comHandle

    def drawStation(self, active):
        # self.stationCount += 1
        if active == self.stationCount:
            bgc = "#D5F5E3"
        else:
            bgc = "#E5E7E9"

        canvas = tk.Canvas(
            self.scanResultsPane,
            relief="raised",
            borderwidth=2,
            width=int(self.mainWindowWidth / 4),
            height=int(self.mainWindowHeight * 0.075),
            bg=bgc,
        )
        xpos = canvas.winfo_width() - 10
        ypos = 50
        canvas.create_text(
            xpos,
            ypos,
            anchor="e",
            text=f"Station {self.stationCount}",
            font=("Arial", 16),
            fill="black",
        )
        canvas.pack()
        self.root.update()
        self.canvases.append(canvas)

    def redrawStation(self, id, type):
        self.canvases[id].delete("all")
        self.canvases[id].create_rectangle(
            0,
            0,
            self.canvases[id].winfo_width(),
            self.canvases[id].winfo_height(),
            outline="black",
            width=2,
            fill="#E5E7E9",
        )
        returnValue = bytearray([0, 1, 3, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        if type == 2:
            self.drawTOF(id, returnValue)
        self.drawLabel(id)

    def listDevices(self, frame):
        values = ["Option 1", "Option 2", "Option 3"]
        combobox1 = ttk.Combobox(self.scanResultsPane, values=values)
        combobox1.grid(row=0, column=0)
        # combobox1.pack()
        combobox2 = ttk.Combobox(self.scanResultsPane, values=values)
        combobox2.grid(row=1, column=0)
        # combobox2.pack()

    def drawTOF(self, index, values):
        offset = 10
        self.rect = {}
        self.oval = {}
        self.cellwidth = 10
        self.cellheight = 10
        for column in range(4):
            for row in range(4):
                colr = values[(column * 4) + (row)]
                x1 = column * self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                x1 += offset
                x2 += offset
                y1 += offset
                y2 += offset
                # if index == 4:
                #     color = "#90EE90"
                # else:
                #     color = "white"
                color = "white"

                self.rect[row, column] = self.canvases[index].create_rectangle(
                    x1, y1, x2, y2, fill=color, tags="rect"
                )
                fillcolor = "white"
                self.oval[row, column] = self.canvases[index].create_oval(
                    x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill=fillcolor, tags="oval"
                )
        # xpos = self.canvases[index].winfo_width() - 10
        # ypos = 50
        # text_id = self.canvases[index].create_text(
        #     xpos, ypos, anchor="e", text=f"Station {index+1}", font=("Arial", 16)
        # )
        # self.canvases[index].tag_raise(text_id)
        # self.canvases[index].itemconfig(text_id, fill="black")

    def drawLabel(self, station):
        xpos = self.canvases[station].winfo_width() - 10
        ypos = 50
        text_id = self.canvases[station].create_text(
            xpos,
            ypos,
            anchor="e",
            text=f"Station {station+1}",
            font=("Arial", 16),
            fill="black",
        )
        self.canvases[station].tag_raise(text_id)
        self.canvases[station].itemconfig(text_id, fill="black")

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

    async def performScan(self, port):
        for j in range(1, 8):
            value_encoded = bytearray([0xA5, 0x08, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00])
            value_encoded[2] = j
            value = port.PktEncode(value_encoded)
            # await port.pollWriteController(value)
            await asyncio.sleep(0.2)
            # result = await port.pollReadController()
            self.stationCount += 1
            activeStation = 3
            # returnValue = port.PktDecode(result)
            returnValue = bytearray(
                [0, 1, 3, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            )
            print(", ".join(f"{byte:02x}" for byte in returnValue))
            self.drawStation(activeStation)
            if returnValue[3] == 0x02:
                self.drawTOF(j - 1, returnValue)
            self.drawLabel(j - 1)


async def main():
    root = tk.Tk()
    GUI = MainGUI(root)
    GUI.root = root
    comPort = serialPolling("/dev/ttyS1", 115200, 1)
    GUI.setlocalCOM(comPort)
    GUI.saveValues(root, GUI)

    # stationCount = 0
    activeStation = 0

    while True:
        root.update_idletasks()
        root.update()
        # if scan requested
        if GUI.scanRequested == True:
            GUI.scanRequested = False
            await GUI.performScan(comPort)
            root.update()
            activeStation = 1

        value_encoded = bytearray([0xA5, 0x08, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00])
        value = comPort.PktEncode(value_encoded)
        # await comPort.pollWriteController(value)
        await asyncio.sleep(0.2)
        # result = await comPort.pollReadController()
        await asyncio.sleep(2)
        if activeStation == 1:
            activeStation = 0
            GUI.redrawStation(2, 2)


if __name__ == "__main__":
    asyncio.run(main())
