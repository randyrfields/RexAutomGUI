import tkinter as tk
import customtkinter
import time
from rexserial import serialPolling
from enum import Enum


class SysControlCommands(Enum):
    NOP = 0
    GETSTATUS = 1


class Station:

    def __init__(self, mainWindow):

        self.mainWindow = mainWindow
        self.totalNumberStations = 0
        self.serial = serialPolling

    def performScan(self):
        for x in range(0, 8):
            self.serial.Poll(x, SysControlCommands.GETSTATUS)
