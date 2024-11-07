import serial
import time


# Configure the serial port
port = '/dev/ttyS1'  # Replace with your serial port
baudrate = 115200    # Replace with your baud rate
timeout = 1          # Timeout for read operations in seconds

# try:
#     # Open the serial port
#     ser = serial.Serial(port, baudrate, timeout=timeout)

#     count = 0
#     while ( count < 3 ):
#         print("Pass...")
#         # Write data to the serial port
#         ser.write(b'Hello, Serial Port!\n')
#         count = count + 1
#         time.sleep(3)

#     print("Write Complete.")
#     # Read data from the serial port
#     # response = ser.readline().decode('utf-8').strip()
#     # print(f"Received: {response}")

# finally:
#     # Close the serial port
#     ser.close()


class serialPolling:

    def __init__(self, port, baud, timeout):
        # Open serial port
        try:
            self.ser = serial.Serial(port=port, bytesize=serial.EIGHTBITS, baudrate=baud, timeout=timeout)
            self.running = True
        except serial.SerialException as e:
            # Send message to GUI
            self.errorcode = e


    async def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()


    async def pollReadController(self):
        # Transmit
        if self.running:
            if self.ser and self.ser.in_waiting > 0:
                data = self.ser.read(self.ser.in_waiting)
                return data
            
    async def pollWriteController(self, data):
        if self.ser:
            self.ser.write(data)
            print(data)

    # COBS encode
    def  PktEncode(self, data: bytes):

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
            decoded.extend(data[block_start + 1:block_end])

            if block_size < 0xFF:
                decoded.append(0)

            block_start = block_end

        return bytes(decoded)
