import threading
import time
import asyncio


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

    async def mainTask(self):
        self.gui.showStation(7)
        while True:
            print("Main Thread")

            await self.scanTask()
            for i in range(0, 7):
                if self.station.nodeStatus[i][0] == 1:
                    self.gui.station_buttons[i].configure(fg_color="green")
                else:
                    self.gui.station_buttons[i].configure(fg_color="#4169E1")
