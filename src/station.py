import tkinter as tk
import customtkinter
import time
import struct
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
        for i in range(0, 8):
            row = []
            for j in range(48):
                row.append(0)
            self.nodeStatus.append(row)

    async def performScan(self):
        rawData = []
        for x in range(1, 8):
            cmd = SysControlCommands.GETSTATUS
            result = await self.serial.Poll(x, cmd.value)
            # result = bytes([0xA7, 0x29, 0x01, 0x0A, 0x00]) + bytes([0x00] * 27)
            if result[3] == 0x05:
                self.nodeStatus[x - 1] = list(result[2:8])
            else:
                self.nodeStatus[x - 1] = list(result[2:5])
                # self.mainWindow.TOFData.append(list(result[5:37]))
                rawData.append(list(result[5:37]))
                formatString = "<H"
                self.mainWindow.TOFData[x - 1] = [
                    struct.unpack(formatString, rawData[i : i + 2])[0]
                    for i in range(0, 32, 2)
                ]
                # self.mainWindow.TOFData[x - 1] = list(result[5:37])
                print(hex(self.mainWindow.TOFData[x - 1]))
