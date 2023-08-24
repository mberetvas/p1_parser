import serial
import argparse
from tabulate import tabulate

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Replace 'COM1' with your serial port

# Create a dictionary to store the parsed data
parsed_data = {}

# Read data from the serial port
while True:
    data = ser.readline().decode('utf-8').strip()  # Assuming the data is in UTF-8 format

    # Check if the data starts with an OBIS reference
    if data.startswith('0-0:96.1.1'):
        parts = data.split(' ', 1)
        if len(parts) == 2:
            obis_reference, value = parts
            parsed_data['Equipment Identifier'] = value

    elif data.startswith('1-0:1.8.1'):
        parts = data.split(' ', 1)
        if len(parts) == 2:
            obis_reference, value = parts
            parsed_data['Meter Reading (Normal Tariff)'] = value

    # Add more conditions for other OBIS references as needed

    # Check if the data transmission is complete
    if data.startswith('!'):
        break

# Close the serial port
ser.close()

# Function to display data with tabulate
def display_tabulated_data(data_dict):
    table_data = [(key, value) for key, value in data_dict.items()]
    print(tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse and display serial data')
    parser.add_argument('-V', '--view', action='store_true', help='Display data with tabulate')
    args = parser.parse_args()

    if args.view:
        display_tabulated_data(parsed_data)
    else:
        for key, value in parsed_data.items():
            print(f'{key}: {value}')
