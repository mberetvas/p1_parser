import serial
import re
import pandas as pd


# Dict with obiscode description
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
                    print("\n","end of data","\n\n\n")
                    data = {}

                line = line.strip(")\r")

                x = line.split("(")
                try:
                    for item in x[1:]:
                        stripped_item = item.strip(")")
                        values = stripped_item.split("*")
                        print("\n",values,"\n")
                        
                        if len(values) < 3:
                                data[obiscodes[x[0]]] = values[0]
                        else:
                            data[obiscodes[x[0]]] = stripped_item
                except:
                    if debug == True:
                        print("did not find corresponding obiscode:", x[0],"\n")
                    continue

if __name__ == '__main__':
    debug = False
    main()