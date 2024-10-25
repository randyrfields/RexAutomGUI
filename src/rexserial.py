import serial
import time


# Configure the serial port
port = '/dev/ttyS1'  # Replace with your serial port
baudrate = 115200    # Replace with your baud rate
timeout = 1          # Timeout for read operations in seconds

try:
    # Open the serial port
    ser = serial.Serial(port, baudrate, timeout=timeout)

    count = 0
    while ( count < 3 ):
        print("Pass...")
        # Write data to the serial port
        ser.write(b'Hello, Serial Port!\n')
        count = count + 1
        time.sleep(3)

    print("Write Complete.")
    # Read data from the serial port
    # response = ser.readline().decode('utf-8').strip()
    # print(f"Received: {response}")

finally:
    # Close the serial port
    ser.close()