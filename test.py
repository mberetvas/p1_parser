import serial


# Dict with obiscode description
obiscodes = {
    "0-0:96.1.4":"",
    "0-0:96.1.1":"",
    "0-0:1.0.0":"",
    "1-0:1.8.1":"",
    "1-0:1.8.2":"",
    "1-0:2.8.1":"",
    "1-0:2.8.2":"",
    "0-0:96.14.0":"",
    "1-0:1.4.0":"",
    "1-0:1.6.0":"",
    "0-0:98.1.0":"",
    "1-0:1.7.0":"",
    "1-0:2.7.0":"",
    "1-0:21.7.0":"",
    "1-0:22.7.0":"",
    "1-0:32.7.0":"",
    "1-0:31.7.0":"",
    "0-0:96.3.10":"",
    "0-0:17.0.0":"",
    "1-0:31.4.0":"",
    "0-0:96.13.0":"",
    "0-1:24.1.0":"",
    "0-1:24.2.3":""
}

# Open the serial port
ser = serial.Serial('/dev/ttyUSB0', 115200)

try:
    while True:
        # Read data from the serial port
        data = ser.readline()

        # Optionally, print the data to the console
        print(data.decode('ascii'))

except KeyboardInterrupt:
    print("Capture stopped by user")
finally:
    # Close the serial port and log file
    ser.close()
