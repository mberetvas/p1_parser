import serial
import argparse
from tabulate import tabulate
import time

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Replace 'COM1' with your serial port

# Define a dictionary for OBIS code meanings
# If needed add or comment out obiscodes
obis_codes = {
    "0-0:1.0.0": "Timestamp",
    "0-0:96.3.10": "Switch electricity",
    "0-1:24.4.0": "Switch gas",
    "0-0:96.1.1": "Meter serial electricity",
    "0-1:96.1.1": "Meter serial gas",
    "0-0:96.14.0": "Current rate (1=day,2=night)",
    "0-0:98.1.0":"e-meter ID",
    "1-0:1.6.0": "Maximale afnamepiek van de huidige maand",
    "1-0:1.8.0":"Totale afgenomen energie in kWh",
    "1-0:1.8.1": "Totale afname in kWh dagtarief ",
    "1-0:1.8.2": "Totale afname in kWh nachttarief ",
    "1-0:2.8.0": "Totale geïnjecteerde energie in kWh",
    "1-0:2.8.1": "Totale injectie in kWh dagtarief ",
    "1-0:2.8.2": "Totale injectie in kWh nachttarief ",
    "1-0:21.7.0": "L1 consumption",
    "1-0:41.7.0": "L2 consumption",
    "1-0:61.7.0": "L3 consumption",
    "1-0:1.7.0": "Afgenomen ogenblikkelijk vermogen in kW",
    "1-0:22.7.0": "L1 production",
    "1-0:42.7.0": "L2 production",
    "1-0:62.7.0": "L3 production",
    "1-0:2.7.0": "Geïnjecteerd ogenblikkelijk vermogen in kW",
    "1-0:32.7.0": "L1 voltage",
    "1-0:52.7.0": "L2 voltage",
    "1-0:72.7.0": "L3 voltage",
    "1-0:31.7.0": "L1 current",
    "1-0:51.7.0": "L2 current",
    "1-0:71.7.0": "L3 current",
    "0-1:24.2.3": "Gas consumption",
    "0-0:17.0.0":"limit threshold"
}

# Function to parse data
def parse_data(data):
    parsed_data = {}
    lines = data.strip().split('\n')

    for line in lines:
        parts = line.split('(', 1)
        if len(parts) == 2:
            key, value = parts
            if key in obis_code_meanings:
                parsed_data[key] = value

    return parsed_data

# Function to display data with tabulate
def display_tabulated_data(data_dict):
    table_data = [(obis_code_meanings[key], value) for key, value in data_dict.items()]
    table = tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid', stralign='left', numalign='left')
    table = table.replace('+-', '+').replace('-+', '+').replace('-|', '|').replace('|-', '|')
    
    # Add start and end messages
    header = "P1 Telegram Start"
    footer = "P1 Telegram End"

    print(header.center(len(table.split('\n')[0])))
    print(table)
    print(footer.center(len(table.split('\n')[0])))

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

            # Wait for 1 second before reading the next data
            time.sleep(1)
    except KeyboardInterrupt:
        # Exit the loop gracefully when Ctrl+C is pressed
        pass
    finally:
        # Close the serial port
        ser.close()
