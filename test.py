import serial

# Open the serial port
ser = serial.Serial('/dev/ttyUSB0', 115200)

try:
    while True:
        # Read data from the serial port
        data = ser.readline()

        # Optionally, print the data to the console
        print(data.decode('utf-8'))

except KeyboardInterrupt:
    print("Capture stopped by user")
finally:
    # Close the serial port and log file
    ser.close()
