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

    def updateIcons(self):
        idle = StationStatus.IDLE
        detect = StationStatus.DETECTION
        block = StationStatus.BLOCKED
        for node in range(0, 7):
            status = self.station.nodeStatus[node][0]
            blocked = self.station.nodeStatus[node][5]
            if status == idle.value:
                color = "#4169E1"
                if blocked != False:
                    color = "red"
            elif status == detect.value:
                color = "green"
            elif status == block.value:
                color = "red"
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
            if (self.gui.currentButton > 0) and (self.Update > 10):
                self.Update = 0
                self.gui.showLiveStation()
