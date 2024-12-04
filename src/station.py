import tkinter as tk
import customtkinter
import time
from rexserial import serialPolling
from enum import Enum


class SysControlCommands(Enum):
    NOP = 0
    GETSTATUS = 1


class Station:

    nodeStatus = []

    def __init__(self, mainWindow):

        self.mainWindow = mainWindow
        self.totalNumberStations = 0
        self.serial = serialPolling("/dev/ttyS1", 115200, 1)

        # Create list for status storage
        for i in range(1, 8):
            row = []
            for j in range(8):
                row.append(0)
            self.nodeStatus.append(row)

    async def performScan(self):
        for x in range(1, 8):
            result = await self.serial.Poll(x, SysControlCommands.GETSTATUS)
            # result = bytes([0xA7, 0x08, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00])
            self.nodeStatus[x].insert(0, list(result[2:8]))
            # self.nodeStatus.insert(x, list(result[2:8]))
            # print(self.nodeStatus)
