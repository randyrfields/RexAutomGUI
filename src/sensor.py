import customtkinter
from station import *


class sensorWindow:

    dummyData = [
        20,
        20,
        20,
        20,
        90,
        90,
        90,
        90,
        130,
        130,
        130,
        130,
        190,
        190,
        190,
        190,
        230,
        230,
        230,
        230,
    ]

    def __init__(self, displayBox):
        self.sensorWin = displayBox
        self.canvas = customtkinter.CTkCanvas(
            self.sensorWin,
            relief="raised",
            # borderwidth=2,
            highlightthickness=0,
            bg="lightblue",
        )
        self.canvas.pack(fill="both", expand=True)

    def calculateColor(self, distanceData):
        if distanceData > 300:
            color = "#EE82EE"  # violet
        else:
            if distanceData > 260:
                color = "#4B0082"  # indigo
            else:
                if distanceData > 220:
                    color = "blue"
                else:
                    if distanceData > 180:
                        color = "green"
                    else:
                        if distanceData > 120:
                            color = "yellow"
                        else:
                            if distanceData > 80:
                                color = "orange"
                            else:
                                if distanceData > 40:
                                    color = "red"
                                else:
                                    color = "white"
        return color

    def showSensorMatrix(self):

        self.canvas.delete("all")
        self.canvas.update_idletasks()
        canwidth = self.canvas.winfo_width()
        canheight = self.canvas.winfo_height()
        offsetx = canwidth / 2 - 120
        offsety = canheight / 2 - 120
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
                color = "lightgreen"

                self.rect[row, column] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, tags="rect"
                )
                fillcolor = self.calculateColor(
                    self.dummyData[15 - ((row * 4) + column)]
                )  # "#EE82EE"
                self.oval[row, column] = self.canvas.create_oval(
                    x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill=fillcolor, tags="oval"
                )

        # self.canvas.create_rectangle(25, 25, 75, 75, fill="blue")
