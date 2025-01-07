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

    def __init__(self, gui, station):
        self.station = station
        self.gui = gui
        mainThread = threading.Thread(
            target=asyncio.run, args=(self.mainTask(),), daemon=True
        )
        mainThread.start()

    async def scanTask(self):
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
    #  * [5:36] TOF data

    def updateIcons(self):
        idle = StationStatus.IDLE
        detect = StationStatus.DETECTION
        block = StationStatus.BLOCKED
        blocked = False
        for node in range(0, 7):
            status = self.station.nodeStatus[node][0]
            if self.station.nodeStatus[node][2]:
                blocked = True
            if status == idle.value:
                color = "#4169E1"
                if blocked != False:
                    color = "red"
            elif status == detect.value:
                color = "green"
            else:
                color = "gray"

            self.gui.station_buttons[node].configure(fg_color=color)

    async def mainTask(self):
        self.gui.showStation(7)
        while True:
            print("Main Thread")
            await self.scanTask()
            self.updateIcons()
            self.Update += 1
            if (self.gui.currentButton < 8) and (self.Update > 10):
                self.Update = 0
                self.gui.showLiveStation()
