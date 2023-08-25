import serial
import re
import pandas as pd

# Dict with obiscode description
obiscodes = {
    "0-0:96.1.4":"verson_info",  # Versie informatie xxxyy waar xxx=dsmr p1 versie en yy=e-MUCs-h versie
    "0-0:96.1.1":"equipment_id", # Hex encoded equip. id according to DIN 43863-5
    "0-0:1.0.0":"timestamp", # Timestamp YYMMDDhhmmssX X is S=Summer W=winter
    "1-0:1.8.1":"totaal_verbruik_dagtarief",
    "1-0:1.8.2":"totaal_verbruik_nachttarief",
    "1-0:2.8.1":"totaal_injectie_dagtarief",
    "1-0:2.8.2":"Totale_injectie_nachttarief",
    "0-0:96.14.0":"Tarief_indicatie", # tarief_indicatie
    "1-0:1.4.0":"gemmiddeld_verbruik", # Gemmiddeld verbruik kw
    "1-0:1.6.0":"piekvermogen_huidige_maand", # Maximum piekvermogen voor huidige maand
    "0-0:98.1.0":"piekvermogen _van_laatste_13_maanden",
    "1-0:1.7.0":"actief_verbruik", # actief verbruik in kw
    "1-0:2.7.0":"actief_injectie", # actieve injectie in kw
    "1-0:21.7.0":"instant_vermogen_L1+P", # instantaneous active power L1 +P
    "1-0:22.7.0":"instant_vermogen_L1-P", # instantaneous active power L1 -P
    "1-0:32.7.0":"spanning", # instantaneous voltage
    "1-0:31.7.0":"stroom", # instantaneous current
    "0-0:96.3.10":"stand_zekering", # Breaker state 0=Disconnected 1=connected 3=ready for connection
    "0-0:17.0.0":"Limiter_threshold", # limiter_threshold
    "1-0:31.4.0":"fuse_threshold", # fuse_treshold
    "0-0:96.13.0":"Text_Messag", # (for future use)
    "0-1:24.1.0":"Device_type", # device-type
    "0-1:24.4.0":"gasklep_stand", # gasklep_stand
    "0-1:24.2.3":"gas_verbruik" # Last value of 'not temperature corrected' gas volume in m³,including decimal values and capture time
}

# Initialize a dictionary to store values for each OBIS code
values_dict = {}

# Initialize a dictionary specifically for "1-0:1.6.0" with lists to store multiple values
obis_1_6_0_values = {}

# Open the serial port
with serial.Serial('/dev/ttyUSB0', 115200) as ser:

    try:
        while True:
            # Read data from the serial port
            data = ser.readline().decode('ascii')

            # Define a regular expression pattern to extract values
            pattern = r'(\d+-\d+:\d+\.\d+\.\d+)\(([^)]+)\)'

            # Use re.finditer to find and extract values from the received data
            for match in re.finditer(pattern, data):
                obis_code = match.group(1)
                value = match.group(2)

                # Check if the OBIS code is already in the dictionary
                if obis_code in obiscodes:
                    description = obiscodes[obis_code]

                    # Check if it's "1-0:1.6.0"
                    if obis_code == "1-0:1.6.0":
                        # Append the value to the list
                        if description in obis_1_6_0_values:
                            obis_1_6_0_values[description].append(value)
                        else:
                            obis_1_6_0_values[description] = [value]
                    else:
                        # For other OBIS codes, store the value as usual
                        values_dict[description] = value

            # Print the values_dict
            if values_dict:
                print("\nOther Values:", values_dict)

            # Print the values for "1-0:1.6.0" if they exist
            if obis_1_6_0_values:
                print("\n1-0:1.6.0 Values:", obis_1_6_0_values)

    except KeyboardInterrupt:
        print("Capture stopped by user")