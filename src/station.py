import tkinter as tk
import customtkinter
from functools import partial


class Station:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.station_frames = []
        self.station_buttons = []
        self.station_button = []

    def button_click(self, index):
        print(f"Button Click = {index}")

    def showStation(self):
        self.outer_frame = customtkinter.CTkFrame(self.mainWindow.station_frame)
        self.outer_frame.grid(row=1, column=2, padx=5, pady=5)

        # Create the stations

        # for x in range(1, 8):
        #     canvas = customtkinter.CTkCanvas(
        #         outer_frame,
        #         width=280,
        #         height=75,
        #         highlightthickness=2,
        #         highlightbackground="black",
        #     )
        #     canvas.pack(side="top")
        #     self.canvases.append(canvas)

        for x in range(0, 7):
            station_frame = customtkinter.CTkFrame(
                self.outer_frame, border_color="black"
            )
            self.station_frames.append(station_frame)
            self.station_frames[x].grid(row=x + 1, padx=5, pady=5)
            self.station_button.append(
                customtkinter.CTkButton(
                    self.station_frames[x],
                    text=f"Station {x+1}",
                    command=partial(self.button_click, x),
                    width=200,
                    height=90,
                    fg_color=#4169E1,
                )
            )
            self.station_buttons.append(self.station_button[x])
            self.station_button[x].pack()

    def showStation_old(self):

        canvas = customtkinter.CTkCanvas(
            self.mainWindow.station_frame,
            relief="raised",
            borderwidth=2,
            # width=int(self.mainWindow.width / 4),
            # height=int(self.mainWindow.height * 0.075),
            width=int(200),
            height=int(100),
            bg="#E5E7E9",
        )
        xpos = canvas.winfo_width() - 10
        ypos = 50
        canvas.create_text(
            xpos,
            ypos,
            anchor="e",
            text=f"Station {5}",
            font=("Arial", 16),
            fill="black",
        )
        canvas.grid(column=2, row=1)
