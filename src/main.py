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
    stationSettings = []
    stationNames = []
    stationName = ""
    stationOrderList = ""
    switch = None

    def __init__(self):
        super().__init__()

        self.station_frames = []
        self.station_buttons = []
        self.station_button = []
        self.quantity_entry = []
        self.address_entry = []
        self.address = []
        self.stationOrder = customtkinter.StringVar(value="1,2,3,4,5,6,7")
        self.addressSelect = []

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
        self.attributes("-fullscreen", True)

        self.assets_dir = Path(__file__).parent.parent / "assets"
        self.logo_dir = os.path.join(self.assets_dir, "Rexair-LLC.png")
        self.image = Image.open(self.logo_dir)
        ctk_image = customtkinter.CTkImage(light_image=self.image, size=(120, 75))

        # configure grid layout (4x8)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0, 2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((3, 4, 5, 6, 7), weight=0)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Station Control",
            font=customtkinter.CTkFont("Consolar", size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            command=partial(self.sidebar_button_event, "Start"),
            text="Start",
            height=80,
            font=("Consolar", 25, "bold"),
            fg_color="#4169E1",
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        # self.sidebar_button_2 = customtkinter.CTkButton(
        #     self.sidebar_frame,
        #     command=partial(self.sidebar_button_event, "Setup"),
        #     text="Setup",
        #     height=80,
        #     font=("Consolar", 25, "bold"),
        #     fg_color="#4169E1",
        # )
        # self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame,
            command=partial(self.sidebar_button_event, "Save"),
            text="Save",
            height=80,
            font=("Consolar", 25, "bold"),
            fg_color="#4169E1",
        )
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.autoRestartcheckBox = customtkinter.CTkCheckBox(
            self.sidebar_frame, text="Auto Restart"
        )
        self.autoRestartcheckBox.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_4 = customtkinter.CTkButton(
            self.sidebar_frame,
            command=partial(self.sidebar_button_event, "Reset"),
            text="Reset",
            height=40,
            font=("Consolar", 25, "bold"),
            fg_color="#4169E1",
        )
        self.sidebar_button_4.grid(row=5, column=0, padx=20, pady=10)

        self.sidebar_button_5 = customtkinter.CTkButton(
            self.sidebar_frame,
            command=partial(self.sidebar_button_event, "Restore"),
            text="Restore",
            height=40,
            font=("Consolar", 25, "bold"),
            fg_color="#4169E1",
        )
        self.sidebar_button_5.grid(row=6, column=0, padx=20, pady=10)
        
        self.sidebar_button_6 = customtkinter.CTkButton(
            self.sidebar_frame,
            command=partial(self.sidebar_button_event, "Update"),
            text="Update",
            height=40,
            font=("Consolar", 25, "bold"),
            fg_color="#4169E1",
        )
        self.sidebar_button_6.grid(row=7, column=0, padx=20, pady=10)

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="> ")
        self.entry.grid(
            row=3, column=1, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20), pady=(20), sticky="nsew")
        self.terminal = Terminal(self.textbox)

        self.displayBox = customtkinter.CTkFrame(self, fg_color="lightblue")
        self.displayBox.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.displaySensor = sensorWindow(self.displayBox)

        # Station Display
        self.station_frame = customtkinter.CTkFrame(self, width=540, corner_radius=0)
        self.station_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        # self.station_frame.grid_rowconfigure(4, weight=1)
        self.station_label = customtkinter.CTkLabel(
            self.station_frame,
            text="Sequence      Station        Qty  ",
            font=customtkinter.CTkFont("Consolas", size=20, weight="bold"),
        )
        self.station_label.grid(row=0, column=2, padx=20, pady=(20, 10))
        self.station_label.configure(width=540)

        for _ in range(7):
            self.stationNames.append(customtkinter.StringVar())

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
        if value == "Start":
            print("Start Button click")
            self.sysController.stationReset = True
        elif value == "Setup":
            print("Setup Button click")
            self.sysController.stationSendSetup = True
        elif value == "Save":
            print("Save Button click")
            self.sysController.stationSaveAll = True
        else:
            print("Calibrate")
            self.sysController.stationCalibrate = True
            # for i in range(7):
            #     print("Quantity=", self.quantity_entry[i].get())

    def addressSelectChange(self, choice, index, id):
        for i in range(7):
            print(self.addressSelect[i].get())
        # print("Station Index ", index, id, choice, i, self.station_buttons[1])
        # self.station_buttons[1].configure(fg_color="red")
        # print("Done")

    def showStation(self, number):

        self.outer_frame = customtkinter.CTkFrame(self.station_frame)
        self.outer_frame.grid(row=1, column=2, padx=5, pady=5)

        for x in range(0, number):
            self.station_frame = customtkinter.CTkFrame(
                self.outer_frame, border_color="black"
            )

            self.station_frames.append(self.station_frame)
            self.station_frames[x].grid(row=x + 1, padx=5, pady=5)
            #
            addressVar = customtkinter.StringVar(value=str(x + 1))
            self.addressSelect.append(
                customtkinter.CTkComboBox(
                    self.station_frames[x],
                    values=["-", "1", "2", "3", "4", "5", "6", "7"],
                    variable=addressVar,
                    width=70,
                    command=lambda choice: self.addressSelectChange(
                        choice, x, self.addressSelect[x]
                    ),
                )
            )
            self.addressSelect[x].pack(side="left", padx=20, pady=10)

            self.station_button.append(
                customtkinter.CTkButton(
                    self.station_frames[x],
                    text=f"Station",
                    command=partial(self.station_button_click, x),
                    font=("Consolas", 25, "bold"),
                    width=200,
                    height=40,
                    fg_color="#4169E1",
                )
            )
            self.station_buttons.append(self.station_button[x])
            self.station_button[x].pack(side="left")

            self.quantity_entry.append(
                customtkinter.CTkEntry(
                    self.station_frames[x], width=50, justify="center"
                )
            )
            self.quantity_entry[x].insert(0, "1")
            self.quantity_entry[x].pack(side="left", padx=10)

    def openStationForm(self, number):
        self.stationSettings = customtkinter.CTkToplevel()
        self.stationSettings.lift
        self.stationSettings.attributes("-topmost", True)
        self.stationSettings.title(f"Station {number+1}")
        self.stationSettings.geometry("300x400")

        self.stationNames[number] = ""
        customtkinter.CTkLabel(self.stationSettings, text="Station Name: ").pack(pady=5)
        self.stationName = customtkinter.CTkEntry(
            self.stationSettings,
            textvariable=self.stationNames[number],
            width=250,
            height=40,
            border_width=2,
        )
        self.stationName.pack(pady=5)

        saveButton = customtkinter.CTkButton(
            self.stationSettings,
            text="Save",
            height=40,
            width=250,
            font=("Consolas", 25, "bold"),
            command=lambda: self.saveStationInfo(number),
        )
        saveButton.pack(pady=5, side="bottom")

    def saveStationInfo(self, number):
        x = number
        strValue = self.stationName.get()
        strValue = strValue[:12]
        self.station_button[x].configure(text=strValue)
        self.stationSettings.destroy()

    def showLiveStation(self):
        self.displaySensor.showSensorMatrix(
            self.activeNode, self.TOFData[self.activeNode]
        )

    def showText(self, text):
        self.terminal.addTextTerminal(text)

    def clearLiveStation(self):
        self.displaySensor.clear()

    def station_button_click(self, index):
        # selection = self.radio_var.get()
        self.openStationForm(index)

        selection = 2
        # if in diagnostics mode (selection = 2), set active node to button click
        if selection == "2":
            print(f"Button Click = {index}")
            self.activeNode = index

    def setSysController(self, sys):
        self.sysController = sys

    def getRadioButtonStatus(self):
        return self.radio_var.get()

    def getAutoRestartStatus(self):
        return self.autoRestartcheckBox.get()


if __name__ == "__main__":
    gui = GUI()
    station = Station(gui)
    sys = SystemController(gui, station)
    gui.setSysController(sys)
    gui.mainloop()
