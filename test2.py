import serial
import re
import pandas as pd
import crcmod.predefined


# Dict with obiscode description (24)
obiscodes = {
    "0-0:96.1.4":"verson_info",  # Versie informatie xxxyy waar xxx=dsmr p1 versie en yy=e-MUCs-h versie
    "0-0:96.1.1":"equipment_id", # Hex encoded equip. id according to DIN 43863-5
    "0-0:1.0.0":"timestamp", # Timestamp YYMMDDhhmmssX X is S=Summer W=winter
    "1-0:1.8.1":"totaal_verbruik_dagtarief_kwh",
    "1-0:1.8.2":"totaal_verbruik_nachttarief_kwh",
    "1-0:2.8.1":"totaal_injectie_dagtarief_kwh",
    "1-0:2.8.2":"Totale_injectie_nachttarief_kwh",
    "0-0:96.14.0":"Tarief_indicatie", # tarief_indicatie
    "1-0:1.4.0":"gemmiddeld_verbruik_kw", # Gemmiddeld verbruik kw
    "1-0:1.6.0":"piekvermogen_huidige_maand", # Maximum piekvermogen voor huidige maand
    "0-0:98.1.0":"piekvermogen _van_laatste_13_maanden",
    "1-0:1.7.0":"actief_verbruik_kw", # actief verbruik in kw
    "1-0:2.7.0":"actief_injectie_kw", # actieve injectie in kw
    "1-0:21.7.0":"instant_vermogen_L1+P_kw", # instantaneous active power L1 +P
    "1-0:22.7.0":"instant_vermogen_L1-P_kw", # instantaneous active power L1 -P
    "1-0:32.7.0":"spanning_V", # instantaneous voltage
    "1-0:31.7.0":"stroom_A", # instantaneous current
    "0-0:96.3.10":"stand_zekering", # Breaker state 0=Disconnected 1=connected 3=ready for connection
    "0-0:17.0.0":"Limiter_threshold_kw", # limiter_threshold
    "1-0:31.4.0":"fuse_threshold_A", # fuse_treshold
    "0-0:96.13.0":"Text_Messag", # (for future use)
    "0-1:24.1.0":"Device_type", # device-type
    "0-1:24.4.0":"gasklep_stand", # gasklep_stand
    "0-1:24.2.3":"gas_verbruik_m³" # Last value of 'not temperature corrected' gas volume in m³,including decimal values and capture time
}

def checkcrc(p1telegram):
    # Initialize p1contents
    p1contents = True
    
    # check CRC16 checksum of telegram and return False if not matching
    # split telegram in contents and CRC16 checksum (format:contents!crc)
    for match in re.compile(b'\r\n(?=!)').finditer(p1telegram):
        p1contents = p1telegram[:match.end() + 1]
        # CRC is in hex, so we need to make sure the format is correct
        givencrc = hex(
            int(p1telegram[match.end() + 1:].decode('ascii').strip(), 16))
    
    # Make sure p1contents is not None before using it
    if p1contents is not None:
        # calculate checksum of the contents
        calccrc = hex(crcmod.predefined.mkPredefinedCrcFun('crc16')(p1contents))
        # check if given and calculated match
        if debug:
            print(f"Given checksum: {givencrc}, Calculated checksum: {calccrc}")
        if givencrc != calccrc:
            if debug:
                print("Checksum incorrect, skipping...")
            return False
    return True


def main():
    # Open the serial port
    with serial.Serial('/dev/ttyUSB0', 115200) as ser:
        data = {}
        p1telegram = bytearray()

        while True:
            # Read data from the serial port
            p1line = ser.readline()
            p1data = p1line.decode("ascii")
            
            if "/" in p1data:
                p1telegram = bytearray()
            
            p1telegram.extend(p1line)
            
            if "!" in p1data:
                if checkcrc(p1telegram):
                    print("**************crc ok***********************")
            
            lines = p1data.split("\n")
            if debug == True:
                print("\n\n",lines,"\n\n")


            for line in lines:

                if line.startswith("!"):
                    print("*"*65,"\n",'Start Telegram:\n',"*"*65,"\n")
                    for k,v in data.items():
                        print(k," =" ,v)

                    print("\n")
                    print("*"*65,"\n")
                    print("end of data","\n")
                    print("*"*65,"\n\n\n\n")
                    
                    # empty dict data
                    data = {}
                    ser.flush()

                # line = line.strip(")\r")
                # replace ")" and "\r" with empty space
                line = line.replace(")"," ").replace("\r", " ")
                
                # print("line.strip(')\\r')")
                # print(line)
                # print("\n")
                
                x = line.split("(")
                x = [item.replace(")","") for item in x]
                
                # print("\n","line.split")
                # print(x)
                # print("\n")
                # print("first print ",x)

                try:

                    if len(x) < 3:
                        if "*" in x[1]:
                            values = x[1].split("*")
                            # remove all non numbers
                            value = ''.join(c for c in values[0] if c.isdigit() or c == '.')
                            data[obiscodes[x[0]]] = value

                            # data[obiscodes[x[0]]] = values[0]
                        else:
                            # data[obiscodes[x[0]]] = x[1]
                            # remove all non numbers
                            value = ''.join(c for c in x[1] if c.isdigit() or c == '.')
                            data[obiscodes[x[0]]] = value
                    else:
                        data[obiscodes[x[0]]] = x[1:]

                except:
                    if debug == True:
                        print("did not find corresponding obiscode:", x[0],"\n")
                    continue
            ser.flush()

if __name__ == '__main__':
    debug = False
    main()