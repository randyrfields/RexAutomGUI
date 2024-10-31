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
            self.ser = serial.Serial(port, baud, timeout)
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
            