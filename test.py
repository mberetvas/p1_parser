import serial
import re


# Dict with obiscode description
obiscodes = {
    "0-0:96.1.4":"Versie informatie xxxyy waar xxx=dsmr p1 versie en yy=e-MUCs-h versie", 
    "0-0:96.1.1":"Hex encoded equip. id according to DIN 43863-5",
    "0-0:1.0.0":"Timestamp YYMMDDhhmmssX X is S=Summer W=winter",
    "1-0:1.8.1":"Totale afname dagtarief",
    "1-0:1.8.2":"Totale afname nachttarief",
    "1-0:2.8.1":"Totale injectie dagtarief",
    "1-0:2.8.2":"Totale injectie nachttarief",
    "0-0:96.14.0":"Tarief indicatie",
    "1-0:1.4.0":"Gemmiddeld verbruik kw",
    "1-0:1.6.0":"Maximum piekvermogen voor huidige maand",
    "0-0:98.1.0":"piekvermogen van laatste 13 maanden",
    "1-0:1.7.0":"actief verbruik in kw",
    "1-0:2.7.0":"actieve injectie in kw",
    "1-0:21.7.0":"instantaneous active power L1 +P",
    "1-0:22.7.0":"instantaneous active power L1 -P",
    "1-0:32.7.0":"instantaneous voltage",
    "1-0:31.7.0":"instantaneous current",
    "0-0:96.3.10":"Breaker state 0=Disconnected 1=connected 3=ready for connection",
    "0-0:17.0.0":"Limiter threshold",
    "1-0:31.4.0":"fuse supervision threshold",
    "0-0:96.13.0":"Text Messag (for future use)",
    "0-1:24.1.0":"Device type",
    "0-1:24.4.0":"Valve State",
    "0-1:24.2.3":"Last value of 'not temperature corrected' gas volume in m³,including decimal values and capture time"
}

# Columns te gebruiken voor database
columns = [
    "version information",
    "equipment id",
    "timestamp",
    "Totaal verbruik Dagtarief",
    "Totaal verbruik Nachttarief",
    "Totaal injectie Dagtarief",
    "Totaal injectie Nachttarief",
    "tarief indicatief",
    "gemmiddeld verbruik kw",
    "piekvermogen huidige maand",
    "actief verbruik",
    "actieve injectie",
    "instant actief vermogen L1 +P",
    "instant actief vermogen L1 -P",
    "spanning",
    "stroom",
    "hoofdzekering stand",
    "limiter threshold",
    "fuse supervision threshold",
    "text message",
    "device type",
    "gas klep stand",
    "laatste gas volume m³"
    ]


# Create a dictionary to store values by their respective IDs
values_dict = {}

# Define a regular expression pattern to extract values
pattern = r'(\d+-\d+:\d+\.\d+\.\d+)\(([^)]+)\)'

# Use re.finditer to find and extract values from each line
for match in re.finditer(pattern, data_string):
    obis_code = match.group(1)
    value = match.group(2)
    values_dict[obis_code] = value

# Print the extracted values
for obis_code, value in values_dict.items():
    print(f"ID: {obis_code}, Value: {value}")

# Open the serial port
with serial.Serial('/dev/ttyUSB0', 115200) as ser:

    try:
        while True:
            # Read data from the serial port
            data = ser.readline()

            # Optionally, print the data to the console
            print(data.decode('ascii'))

    except KeyboardInterrupt:
        print("Capture stopped by user")
