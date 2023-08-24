import serial

# Open the serial port
ser = serial.Serial('/dev/ttyUSB0', 115200)

# Open a log file
log_file = open('serial_log.txt', 'a')

try:
    while True:
        # Read data from the serial port
        data = ser.readline()
        
        # Write the data to the log file
        log_file.write(data.decode('utf-8'))  # Assuming data is in UTF-8 encoding
        
        # Optionally, print the data to the console
        print(data.decode('utf-8'))
except KeyboardInterrupt:
    print("Capture stopped by user")
finally:
    # Close the serial port and log file
    ser.close()
    log_file.close()