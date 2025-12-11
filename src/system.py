import threading
import time
import asyncio
import xml.etree.cElementTree as ET
import os
from enum import Enum


class StationStatus(Enum):
    INACTIVE = 0
    IDLE = 1
    DETECTION = 2
    BLOCKED = 3


class SystemController:

    stationReset = False
    stationCalibrate = False
    stationOrderSend = False
    diagScanResults = True
    stationSendSetup = False
    stationSaveAll = False
    newScanDataAvail = False

    def __init__(self, gui, station):
        self.station = station
        self.gui = gui
        mainThread = threading.Thread(
            target=asyncio.run, args=(self.mainTask(),), daemon=True
        )
        mainThread.start()

    def SaveSettings(self):
        # Write settings to disk
        cfg = ET.Element("config")
        ET.SubElement(cfg, "node_order").text = "1,2,3,4,5,6,7"
        ET.SubElement(cfg, "auto_restart").text = "0"
        ET.SubElement(cfg, "quantity").text = "1,1,1,1,1,1,1"
        tree = ET.ElementTree(cfg)

        os.makedirs("/opt/cfg", exist_ok=True)
        with open("/opt/cfg/settings.cfg", "wb") as file:
            tree.write(file, encoding="utf-8", xml_declaration=True)

    async def scanDiags(self):
        result = 0
        if self.diagScanResults:
            result = await self.station.scanResults()
            return result

    async def scanTask(self):
        if self.stationReset:
            await self.station.resetStations()
            self.stationReset = False
        # elif self.stationCalibrate:
        #     await self.station.calibrateStations()
        #     self.stationCalibrate = False
        elif self.stationOrderSend:
            await self.station.sendStationOrder()
            self.stationOrderSend = False
        elif self.stationSendSetup:
            await self.station.sendStationSetup()
            self.stationSendSetup = False
        elif self.stationSaveAll:
            self.SaveSettings()
            self.stationSaveAll = False
        else:
            await self.station.performScan()
            self.newScanDataAvail = True

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
        inactive = StationStatus.INACTIVE
        idle = StationStatus.IDLE
        detect = StationStatus.DETECTION
        block = StationStatus.BLOCKED
        blocked = False
        self.gui.activeNode = 15
        for node in range(0, 7):
            if self.gui.addressSelect[node].get() == "-":
                color = "gray"
            else:
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
                    self.gui.activeNode = node
                    color = "green"
                else:
                    color = "gray"

            self.gui.station_buttons[node].configure(fg_color=color)

        return

    async def mainTask(self):

        stat = 1
        self.gui.showStation(7)
        while True:

            await self.scanTask()
            print("Scan")
            if self.gui.stopApp:
                break

            if stat == 1:
                if self.newScanDataAvail:
                    self.updateIcons()
                    self.newScanDataAvail = False
                else:
                    continue
                if self.gui.activeNode < 8:
                    nodeType = self.station.nodeStatus[self.gui.activeNode][3]
                    if nodeType == 0x0A:
                        self.gui.showLiveStation()
                    else:
                        self.gui.clearLiveStation()

                else:
                    self.gui.clearLiveStation()
                    if self.gui.getAutoRestartStatus() == 1:
                        print("Auto Restart Sent")
                        self.stationReset = True
                        time.sleep(1)

            else:
                if self.gui.activeNode < 8:
                    nodeType = self.station.nodeStatus[self.gui.activeNode][3]
                    if nodeType == 0x0A:
                        self.gui.showLiveStation()
                    else:
                        self.gui.clearLiveStation()

                data = await self.scanDiags()
                # print(chr(27) + "[2J")
                # print("Node:  0  1  2  3  4  5  6  7")
                # print("     ", end=" ")
                # try:
                #     for i in range(3, 11):
                #         print(f"{data[i]:2d}", end=" ")
                # except:
                #     print("Data error")
                # print("curButton, NdType=", self.gui.activeNode, nodeType)
                # print(" ")
                time.sleep(1)
