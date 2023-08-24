import serial
import re

# Dict with obiscode description
obiscodes = {
    "0-0:96.1.4":"Versie informatie xxxyy waar xxx=dsmr p1 versie en yy=e-MUCs-h versie",  #verson_info
    "0-0:96.1.1":"Hex encoded equip. id according to DIN 43863-5", #equipment_id
    "0-0:1.0.0":"Timestamp YYMMDDhhmmssX X is S=Summer W=winter", #timestamp
    "1-0:1.8.1":"Totale afname dagtarief", #totaal_verbruikte_dagtarief
    "1-0:1.8.2":"Totale afname nachttarief", #totaal_verbruikte_nachttarief
    "1-0:2.8.1":"Totale injectie dagtarief", #totaal_injectie_dagtarief
    "1-0:2.8.2":"Totale injectie nachttarief", #totaal_injectie_nachttarief
    "0-0:96.14.0":"Tarief indicatie", #tarief_indicatie
    "1-0:1.4.0":"Gemmiddeld verbruik kw", #gemmiddeld_verbruik
    "1-0:1.6.0":"Maximum piekvermogen voor huidige maand", #piekvermogen_huidige_maand
    "0-0:98.1.0":"piekvermogen van laatste 13 maanden",
    "1-0:1.7.0":"actief verbruik in kw", # actief_verbruik
    "1-0:2.7.0":"actieve injectie in kw", # actief_injectie
    "1-0:21.7.0":"instantaneous active power L1 +P", # instant_vermogen_L1+P
    "1-0:22.7.0":"instantaneous active power L1 -P", # instant_vermogen_L1-P
    "1-0:32.7.0":"instantaneous voltage", # spanning
    "1-0:31.7.0":"instantaneous current", # stroom
    "0-0:96.3.10":"Breaker state 0=Disconnected 1=connected 3=ready for connection", # "stand_zekering"
    "0-0:17.0.0":"Limiter threshold", # limiter_threshold
    "1-0:31.4.0":"fuse supervision threshold", # fuse_treshold
    "0-0:96.13.0":"Text Messag (for future use)",
    "0-1:24.1.0":"Device type", # device-type
    "0-1:24.4.0":"Valve State", # gasklep_stand
    "0-1:24.2.3":"Last value of 'not temperature corrected' gas volume in m³,including decimal values and capture time" # gas_verbruik
}

# Create a dictionary to store values by their respective IDs
values_dict = {}

# Open the serial port
with serial.Serial('/dev/ttyUSB0', 115200) as ser:

    try:
        while True:
            # Read data from the serial port
            data = ser.readline().decode('ascii')

            # Print the received data
            # print(data)

            # Define a regular expression pattern to extract values
            pattern = r'(\d+-\d+:\d+\.\d+\.\d+)\(([^)]+)\)'

            # Use re.finditer to find and extract values from the received data
            for match in re.finditer(pattern, data):
                obis_code = match.group(1)
                value = match.group(2)
                if obis_code in obiscodes:
                    description = obiscodes[obis_code]
                    values_dict[description] = value

            # Optionally, print the extracted values
            for description, value in values_dict.items():
                print(f"Description: {description}, Value: {value}")

    except KeyboardInterrupt:
        print("Capture stopped by user")
