import tkinter as tk
import customtkinter
import time
from rexserial import serialPolling
from enum import Enum


class SysControlCommands(Enum):
    NOP = 0
    GETSTATUS = 1


class Station:

    nodeStatus = [8][32]

    def __init__(self, mainWindow):

        self.mainWindow = mainWindow
        self.totalNumberStations = 0
        self.serial = serialPolling("/dev/ttyS1", 115200, 1)

    async def performScan(self):
        for x in range(1, 8):
            print("Loop")
            result = await self.serial.Poll(x, SysControlCommands.GETSTATUS)
            self.nodeStatus[x][0] = list(result[4:7])
