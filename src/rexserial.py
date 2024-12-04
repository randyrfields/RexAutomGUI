import serial
import time


# Configure the serial port
port = "/dev/ttyS1"  # Replace with your serial port
baudrate = 115200  # Replace with your baud rate
timeout = 1  # Timeout for read operations in seconds


class serialPolling:

    def __init__(self, port, baud, timeout):
        # Open serial port
        try:
            self.ser = serial.Serial(
                port=port, bytesize=serial.EIGHTBITS, baudrate=baud, timeout=timeout
            )
            self.running = True
        except serial.SerialException as e:
            # Send message to GUI
            self.errorcode = e

    async def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    # |Header|Length|Command|NodeID|Data|0x00|
    async def pollReadController(self):
        # Transmit
        if self.running:
            if self.ser and self.ser.in_waiting > 0:
                data = self.ser.read(self.ser.in_waiting)
                return data

    async def pollWriteController(self, data):
        if self.ser:
            self.ser.write(data)

    # COBS encode
    def PktEncode(self, data: bytes):

        length = len(data)
        encoded = bytearray()

        block_start = 0
        while block_start < length:
            block_end = block_start
            while block_end < length and data[block_end] != 0:
                block_end += 1

            block_size = block_end - block_start + 1
            encoded.append(block_size)
            encoded.extend(data[block_start:block_end])
            block_start = block_end + 1

        encoded.append(0)

        return bytes(encoded)

    # COBS decode
    def PktDecode(self, data: bytes) -> bytes:
        length = len(data)
        decoded = bytearray()

        block_start = 0
        while block_start < length:
            block_size = data[block_start]
            if block_size == 0:
                break

            block_end = block_start + block_size
            decoded.extend(data[block_start + 1 : block_end])

            if block_size < 0xFF:
                decoded.append(0)

            block_start = block_end

        return bytes(decoded)

    async def Poll(self, node, command):
        cmd = []
        response = []
        # Request status
        address = 0xA0 | node
        cmd.append(command.value)
        cmd.insert(0, address)
        cmd.insert(1, 3)
        value = bytes(cmd)
        print("V=", value)
        requestStatusPkt = self.PktEncode(value)
        print("P=", requestStatusPkt)
        # Send packet
        await self.pollWriteController(requestStatusPkt)
        time.sleep(0.9)
        response = await self.pollReadController()
        dcdpkt = self.PktDecode(response)

        return dcdpkt
