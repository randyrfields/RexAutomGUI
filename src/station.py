import tkinter as tk
import struct
from rexserial import serialPolling
from enum import Enum


class SysControlCommands(Enum):
    NOP = 0
    GETSTATUS = 1
    RESETSTATIONS = 15
    SCANRESULTS = 16


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

            try:
                result = await self.serial.Poll(x, cmd.value)
            except:
                result = bytes([0xA7, 0x29, 0x01, 0x05, 0x00]) + bytes([0x00] * 32)

            self.mainWindow.stationType.insert(x, result[3])

            if result[3] == 0x05:
                self.nodeStatus[x - 1] = list(result[0:8])
            else:
                self.nodeStatus[x - 1] = list(result[0:5])
                # self.mainWindow.TOFData.append(list(result[5:37]))
                rawData = result[5:37]
                if rawData % 2 != 0:
                    print("rawData size ", len(rawData))
                formatString = "<H"
                self.mainWindow.TOFData[x - 1] = [
                    struct.unpack(formatString, rawData[i : i + 2])[0]
                    for i in range(0, 32, 2)
                ]
                # self.mainWindow.TOFData[x - 1] = list(result[5:37])
                # print(self.mainWindow.TOFData[x - 1])

    async def resetStations(self):
        cmd = SysControlCommands.RESETSTATIONS

        try:
            node = 0x0F
            result = await self.serial.Poll(node, cmd.value)
        except:
            result = bytes([0xFF, 0xFF, 0xFF, 0xFF])

        if result[3] == 0xAA:
            # print Success message
            self.mainWindow.terminal.addTextTerminal(
                "System function reset success.\n\r"
            )
        else:
            # print Failed message
            self.mainWindow.terminal.addTextTerminal("System function reset fail.\n\r")

    async def scanResults(self):
        cmd = SysControlCommands.SCANRESULTS

        try:
            node = 0x0F
            result = await self.serial.Poll(node, cmd.value)
        except:
            result = bytes([0xFF, 0xFF, 0xFF, 0xFF])

        return result
