import tkinter
import tkinter.messagebox
import customtkinter
import os
import platform
import threading
import time
from pathlib import Path
from PIL import Image
from functools import partial
from station import Station
from system import SystemController
from terminal import Terminal
from sensor import sensorWindow

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class GUI(customtkinter.CTk):

    TOFData = []
    activeNode = 0
    stationType = []
    sysController = 0
    radio_var = 0

    def __init__(self):
        super().__init__()

        self.station_frames = []
        self.station_buttons = []
        self.station_button = []
        self.quantity_entry = []

        self.TOFData = [[0] * 16 for x in range(8)]
        self.stationType = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # configure window
        self.os = platform.system()
        if self.os == "Windows":
            self.after(0, lambda: self.state("zoomed"))
        else:
            self.after(0, lambda: self.attributes("-zoomed", True))

        self.title("Rexair Automation Controller")
        self.geometry(f"{1100}x{580}")

        self.assets_dir = Path(__file__).parent.parent / "assets"
        self.logo_dir = os.path.join(self.assets_dir, "Rexair-LLC.png")
        self.image = Image.open(self.logo_dir)
        ctk_image = customtkinter.CTkImage(light_image=self.image, size=(120, 75))

        # configure grid layout (4x8)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Station Control",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            command=partial(self.sidebar_button_event, "Reset"),
            text="Reset",
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame,
            command=partial(self.sidebar_button_event, "Calibrate"),
            text="Calibrate",
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.appearance_mode_label = customtkinter.CTkLabel(
        #     self.sidebar_frame, text="Appearance Mode:", anchor="w"
        # )
        # self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        # self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
        #     self.sidebar_frame,
        #     values=["Light", "Dark", "System"],
        #     command=self.change_appearance_mode_event,
        # )
        # self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        # self.scaling_label = customtkinter.CTkLabel(
        #     self.sidebar_frame, text="UI Scaling:", anchor="w"
        # )
        # self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        # self.scaling_optionemenu = customtkinter.CTkOptionMenu(
        #     self.sidebar_frame,
        #     values=["80%", "90%", "100%", "110%", "120%"],
        #     command=self.change_scaling_event,
        # )
        # self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="> ")
        self.entry.grid(
            row=3, column=1, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        # self.main_button_1 = customtkinter.CTkButton(
        #     master=self,
        #     fg_color="transparent",
        #     border_width=2,
        #     text_color=("gray10", "#DCE4EE"),
        # )
        # self.main_button_1.grid(
        #     row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
        # )

        self.logo_frame = customtkinter.CTkFrame(
            self, width=150, fg_color="transparent", corner_radius=0
        )
        self.logo_frame.grid(row=3, column=3, sticky="nsew")
        self.logo_frame.grid_rowconfigure(1, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.logo_frame, image=ctk_image, text=""
        )
        self.logo_label.pack(pady=10)

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20), pady=(20), sticky="nsew")
        self.terminal = Terminal(self.textbox)

        self.displayBox = customtkinter.CTkFrame(self, fg_color="lightblue")
        self.displayBox.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.displaySensor = sensorWindow(self.displayBox)

        self.station_frame = customtkinter.CTkFrame(self, width=340, corner_radius=0)
        self.station_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.station_frame.grid_rowconfigure(4, weight=1)
        self.station_label = customtkinter.CTkLabel(
            self.station_frame,
            text="Stations",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.station_label.grid(row=0, column=2, padx=20, pady=(20, 10))
        self.station_label.configure(width=340)

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(
            row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(
            master=self.radiobutton_frame, text="Scan Options"
        )
        self.label_radio_group.grid(
            row=0, column=2, columnspan=1, padx=10, pady=10, sticky=""
        )

        self.radio_var = customtkinter.StringVar(value="1")
        self.radio_button_1 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var,
            value="1",
            text="Polling Mode",
        )
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="nw")

        self.radio_button_2 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var,
            value="2",
            text="Diagnostics",
        )
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="nw")

        # create slider and progressbar frame , fg_color="transparent"
        self.slider_progressbar_frame = customtkinter.CTkFrame(self)
        self.slider_progressbar_frame.grid(
            row=3, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(
            row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew"
        )

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(
            row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        self.checkbox_1 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame, text="Live Display"
        )
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="nw")
        self.checkbox_2 = customtkinter.CTkCheckBox(
            master=self.checkbox_slider_frame, text="Stop on Error"
        )
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="nw")
        self.checkbox_1.select()
        # self.appearance_mode_optionemenu.set("Dark")
        # self.scaling_optionemenu.set("100%")
        self.progressbar_1.configure(mode="indeterminate")
        self.progressbar_1.start()
        self.textbox.insert(
            "0.0",
            "Rexair Automation\n\n",
        )

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog"
        )
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self, value):
        if value == "Reset":
            print("Reset Button click")
            self.sysController.stationReset = True
        else:
            print("Calibrate Button click")
            self.sysController.stationCalibrate = True
            for i in range(7):
                print("Quantity=", self.quantity_entry[i].get())

    def showStation(self, number):

        self.outer_frame = customtkinter.CTkFrame(self.station_frame)
        self.outer_frame.grid(row=1, column=2, padx=5, pady=5)

        for x in range(0, number):
            self.station_frame = customtkinter.CTkFrame(
                self.outer_frame, border_color="black"
            )

            bgc = "#4169E1"

            self.station_frames.append(self.station_frame)
            self.station_frames[x].grid(row=x + 1, padx=5, pady=5)
            self.station_button.append(
                customtkinter.CTkButton(
                    self.station_frames[x],
                    text=f"Station {x+1}",
                    command=partial(self.station_button_click, x),
                    width=200,
                    height=90,
                    fg_color=bgc,
                )
            )
            self.station_button[x].pack(side="left")
            self.station_buttons.append(self.station_button[x])

            self.quantity_entry.append(
                customtkinter.CTkEntry(self.station_frames[x], width=50)
            )
            self.quantity_entry[x].insert(0, "1")
            self.quantity_entry[x].pack(side="left", padx=10)

    # Not used, clears panel showing stations
    # def clearStations(self):
    #     self.outer_frame.grid_forget()

    def showLiveStation(self):
        self.terminal.clearTerminal()
        # print("ST=", self.stationType)
        self.displaySensor.showSensorMatrix(
            self.activeNode, self.TOFData[self.activeNode]
        )

    def showText(self, text):
        self.terminal.addTextTerminal(text)

    def clearLiveStation(self):
        self.displaySensor.clear()

    def station_button_click(self, index):
        selection = self.radio_var.get()
        print("Button Click ", selection)
        # if in diagnostics mode (selection = 2), set active node to button click
        if selection == "2":
            print(f"Button Click = {index}")
            self.activeNode = index

    def setSysController(self, sys):
        self.sysController = sys

    def getRadioButtonStatus(self):
        return self.radio_var.get()


if __name__ == "__main__":
    gui = GUI()
    station = Station(gui)
    sys = SystemController(gui, station)
    gui.setSysController(sys)
    gui.mainloop()
