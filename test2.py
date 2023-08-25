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

# def main():

    # # Open the serial port
    # with serial.Serial('/dev/ttyUSB0', 115200, xonxoff=1) as ser:
    #     while True:
    #         try:
    #             # Read data from the serial port
    #             p1data = ser.readline().decode("ascii").strip()
                
    #             if "/" in p1data:
    #                 print("Start of telegram:\n")
    #                 print(p1data.split("\n"))

    #             else:
    #                 if "!" in p1data
    #                 print("End of telegram \n")

    #         except KeyboardInterrupt:
    #             print("Capture stopped by user")
    #             ser.close()
                
    # Open the serial port
#     with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
#         telegram = {}
#         while True:
#             try:
#                 # Read data from the serial port
#                 p1data = ser.readline().decode("ascii")
#                 listp1 = p1data.splitlines()[0].strip(")").split("(")
#                 print(listp1)

#             except KeyboardInterrupt:
#                 print("Capture stopped by user")
#                 break

# if __name__ == '__main__':
#     main()

import serial

def main():
    # Open the serial port
    with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
        while True:
            try:
                # Read data from the serial port
                p1data = ser.readline().decode("ascii")
                
                print(p1data)

if __name__ == '__main__':
    main()