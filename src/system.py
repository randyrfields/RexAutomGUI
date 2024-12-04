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
        for node in range(1, 8):
            if self.station.nodeStatus[node][0] == 1:
                self.gui.station_buttons[node].configure(fg_color="#4169E1")
            elif self.station.nodeStatus[node][0] == 2:
                self.gui.station_buttons[node].configure(fg_color="green")
            elif self.station.nodeStatus[node][0] == 3:
                self.gui.station_buttons[node].configure(fg_color="red")
            else:
                self.gui.station_buttons[node].configure(fg_color="gray")

    async def mainTask(self):
        self.gui.showStation(7)
        while True:
            print("Main Thread")
            await self.scanTask()
            self.updateIcons()
