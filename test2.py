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

def main():
    # Open the serial port
    with serial.Serial('/dev/ttyUSB0', 115200) as ser:
        data = {}

        while True:
            # Read data from the serial port
            p1data = ser.readline().decode("ascii")
            
            lines = p1data.split("\n")
            if debug == True:
                print("\n\n",lines,"\n\n")


            for line in lines:

                if "!" in line:
                    for k,v in data.items():
                        print(k," =" ,v)
                    print("end of data","\n\n\n")
                    data = {}

                line = line.strip(")\r")

                x = line.split("(")
                try:
                    data[obiscodes[x[0]]] = [item.strip(")") for item in x[1:]] 
                except:
                    if debug == True:
                        print("did not find corresponding obiscode:", x[0],"\n")
                    continue




if __name__ == '__main__':
    debug = False
    main()


# import serial
# import re
# import logging
# from datetime import datetime

# # Configuration
# SERIAL_PORT = '/dev/ttyUSB0'
# DEBUG_MODE = False

# # Generate a timestamp for the log file name
# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# # Define the log file name with the timestamp
# LOG_FILE_NAME = f"parser_{timestamp}.log"

# # Dict with obiscode description
# obiscodes = {
#     # ... (your obiscodes dictionary)
# }

# def main():
#     # Configure logging
#     logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO, filename=LOG_FILE_NAME)

#     # Open the serial port
#     with serial.Serial(SERIAL_PORT, 115200) as ser:
#         data = {}

#         while True:
#             try:
#                 # Read data from the serial port
#                 p1data = ser.readline().decode("ascii")
                
#                 lines = p1data.split("\n")

#                 for line in lines:
#                     if "!" in line:
#                         process_and_log_data(data)
#                         data = {}
#                     else:
#                         parse_line(line, data)
            
#             except serial.SerialException as e:
#                 logging.error(f"Serial communication error: {e}")

# def process_and_log_data(data):
#     for k, v in data.items():
#         logging.info(f"{k} = {v}")
#     logging.info("End of data\n")
#     # Here, you can add additional processing or logging if needed

# def parse_line(line, data):
#     line = line.strip(")\r")
#     x = line.split("(")
#     try:
#         data[obiscodes[x[0]]] = [item.strip(")") for item in x[1:]] 
#     except KeyError:
#         if DEBUG_MODE:
#             logging.debug(f"Did not find corresponding obiscode: {x[0]}")

# if __name__ == '__main__':
#     main()
