import serial
import argparse
from tabulate import tabulate
import time

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Replace 'COM1' with your serial port

# Function to parse data
def parse_data(data):
    parsed_data = {}
    lines = data.strip().split('\n')

    for line in lines:
        parts = line.split('(', 1)
        if len(parts) == 2:
            key, value = parts
            parsed_data[key] = value

    return parsed_data

# Function to display data with tabulate
def display_tabulated_data(data_dict):
    table_data = [(key, value) for key, value in data_dict.items()]
    print(tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse and display serial data')
    parser.add_argument('-V', '--view', action='store_true', help='Display data with tabulate')
    args = parser.parse_args()

    try:
        while True:
            data = ser.read_until(b'!')
            parsed_data = parse_data(data.decode('utf-8'))

            if args.view:
                display_tabulated_data(parsed_data)
            else:
                for key, value in parsed_data.items():
                    print(f'{key}: {value}')

            # Wait for 1 second before reading the next data
            time.sleep(1)
    except KeyboardInterrupt:
        # Exit the loop gracefully when Ctrl+C is pressed
        pass
    finally:
        # Close the serial port
        ser.close()
