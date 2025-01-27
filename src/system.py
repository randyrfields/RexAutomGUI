import threading
import time
import asyncio
from enum import Enum


class StationStatus(Enum):
    INACTIVE = 0
    IDLE = 1
    DETECTION = 2
    BLOCKED = 3


class SystemController:

    Update = 0
    stationReset = False
    diagScanResults = True

    def __init__(self, gui, station):
        self.station = station
        self.gui = gui
        mainThread = threading.Thread(
            target=asyncio.run, args=(self.mainTask(),), daemon=True
        )
        mainThread.start()

    async def scanDiags(self):
        result = 0
        if self.diagScanResults:
            result = await self.station.scanResults()
            return result

    async def scanTask(self):
        if self.stationReset:
            await self.station.resetStations()
            self.stationReset = False
        else:
            await self.station.performScan()

    #  * [0] 0xAn, n = node id
    #  * [1] 0xsz, sz = packet size before encoding
    #  * [2] 0xst, st = Status: Inactive(0), Idle(1), Detection(2)
    #  * [3] 0xsn, sn = Sensor Type: Unknown(0), EmitterDetector(0x05), TimeofFlight(0x0A)
    #  * [4] 0xsw, sw = Switch state: True = Receiver blocked, False = Receiver not blocked
    #  * For Emitter/Detector type configuration:
    #  * [5] 0xrl, rl = Receiver light state: True = on
    #  * [6] 0xel, el = Emitter light state: True = on
    #  * [7] 0xrb, rb = Receiver Blocked: True = blocked
    #  * For TOF type configuration:
    #  * [5:37] TOF data

    def updateIcons(self):
        idle = StationStatus.IDLE
        detect = StationStatus.DETECTION
        block = StationStatus.BLOCKED
        blocked = False
        self.gui.currentButton = 15
        for node in range(0, 7):
            status = self.station.nodeStatus[node][2]
            if self.station.nodeStatus[node][4]:
                blocked = True
            else:
                blocked = False
            if status == idle.value:
                color = "#4169E1"
                if blocked != False:
                    color = "red"
            elif status == detect.value:
                self.gui.currentButton = node
                color = "green"
            else:
                color = "gray"

            self.gui.station_buttons[node].configure(fg_color=color)

        return

    async def mainTask(self):
        data = [0 * 16]
        Count = 0
        self.gui.showStation(7)
        while True:

            await self.scanTask()

            if self.gui.getRadioButtonStatus() == "1":
                # print("Main Thread")
                self.updateIcons()
                self.Update += 1
                if self.gui.currentButton < 8:
                    print("curButton = ", self.gui.currentButton)
                    print(self.station.nodeStatus[0])
                    print(len(self.station.nodeStatus[self.gui.currentButton]))
                    nodeType = self.station.nodeStatus[self.gui.currentButton][3]
                    if nodeType == 0x0A:
                        self.Update = 0
                        self.gui.showLiveStation()
                    else:
                        self.gui.clearLiveStation()
            else:
                if self.gui.currentButton < 8:
                    nodeType = self.station.nodeStatus[self.gui.currentButton][3]
                    if nodeType == 0x0A:
                        self.Update = 0
                        self.gui.showLiveStation()
                    else:
                        self.gui.clearLiveStation()

                data = await self.scanDiags()
                print(chr(27) + "[2J")
                print("Node:  0  1  2  3  4  5  6  7")
                print("     ", end=" ")
                for i in range(3, 11):
                    print(f"{data[i]:2d}", end=" ")
                print("curButton, NdType=", self.gui.currentButton, nodeType)
                print(" ")
                time.sleep(1)
