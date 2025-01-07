import customtkinter
from station import *


class sensorWindow:

    def __init__(self, displayBox):
        self.sensorWin = displayBox
        self.canvas = customtkinter.CTkCanvas(
            self.sensorWin,
            relief="raised",
            # borderwidth=2,
            highlightthickness=0,
            bg="white",
        )
        self.canvas.pack(fill="both", expand=True)

    def calculateColor(self, distanceData):
        if distanceData > 300:
            color = "#EE82EE"  # violet
        else:
            if distanceData > 1000:
                color = "#4B0082"  # indigo
            else:
                if distanceData > 300:
                    color = "blue"
                else:
                    if distanceData > 250:
                        color = "green"
                    else:
                        if distanceData > 200:
                            color = "yellow"
                        else:
                            if distanceData > 100:
                                color = "orange"
                            else:
                                if distanceData > 50:
                                    color = "red"
                                else:
                                    color = "white"
        return color

    def showSensorMatrix(self, stationNumber, liveData):

        self.canvas.delete("all")
        self.canvas.update_idletasks()
        canwidth = self.canvas.winfo_width()
        canheight = self.canvas.winfo_height()
        offsetx = canwidth / 2 - 120
        offsety = canheight / 2 - 120
        stationText = f"Station {stationNumber+1}"
        self.canvas.create_text(
            (canwidth / 2), 25, text=stationText, font=("Arial", 20, "bold")
        )
        self.rect = {}
        self.oval = {}
        self.cellwidth = 60
        self.cellheight = 60
        for column in range(4):
            for row in range(4):
                x1 = column * self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                x1 += offsetx
                x2 += offsetx
                y1 += offsety
                y2 += offsety
                color = "#C6C0B9"

                self.rect[row, column] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, tags="rect"
                )
                fillcolor = self.calculateColor(
                    liveData[15 - ((row * 4) + column)]
                )  # "#EE82EE"
                self.oval[row, column] = self.canvas.create_oval(
                    x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill=fillcolor, tags="oval"
                )

        # self.canvas.create_rectangle(25, 25, 75, 75, fill="blue")
