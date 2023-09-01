import serial
import crcmod
import time
import re
import pandas
from datetime import datetime, timezone


# Dict with obiscode description (24) to add or remove from database comment line out
obiscodes = {
    #"0-0:96.1.4":"verson_info",  # Versie informatie xxxyy waar xxx=dsmr p1 versie en yy=e-MUCs-h versie
    #"0-0:96.1.1":"equipment_id", # Hex encoded equip. id according to DIN 43863-5
    "0-0:1.0.0":"timestamp", # Timestamp YYMMDDhhmmssX X is S=Summer W=winter
    "1-0:1.8.1":"totaal_verbruik_dagtarief_kwh",
    "1-0:1.8.2":"totaal_verbruik_nachttarief_kwh",
    "1-0:2.8.1":"totaal_injectie_dagtarief_kwh",
    "1-0:2.8.2":"Totale_injectie_nachttarief_kwh",
    "0-0:96.14.0":"Tarief_indicatie", # tarief_indicatie
    "1-0:1.4.0":"gemmiddeld_verbruik_kw", # Gemmiddeld verbruik kw
    "1-0:1.6.0":"piekvermogen_huidige_maand", # Maximum piekvermogen voor huidige maand
    #"0-0:98.1.0":"piekvermogen _van_laatste_13_maanden",
    "1-0:1.7.0":"actief_verbruik_kw", # actief verbruik in kw
    "1-0:2.7.0":"actief_injectie_kw", # actieve injectie in kw
    "1-0:21.7.0":"instant_vermogen_L1+P_kw", # instantaneous active power L1 +P
    "1-0:22.7.0":"instant_vermogen_L1-P_kw", # instantaneous active power L1 -P
    "1-0:32.7.0":"spanning_V", # instantaneous voltage
    "1-0:31.7.0":"stroom_A", # instantaneous current
    #"0-0:96.3.10":"stand_zekering", # Breaker state 0=Disconnected 1=connected 3=ready for connection
    #"0-0:17.0.0":"Limiter_threshold_kw", # limiter_threshold
    #"1-0:31.4.0":"fuse_threshold_A", # fuse_treshold
    #"0-0:96.13.0":"Text_Messag", # (for future use)
    #"0-1:24.1.0":"Device_type", # device-type
    #"0-1:24.4.0":"gasklep_stand" # gasklep_stand
    "0-1:24.2.3":"gas_verbruik_m³" # Last value of 'not temperature corrected' gas volume in m³,including decimal values and capture time
}

# Serial port configuration dictionary
SERIAL_CONFIG = {
    'port': '/dev/ttyUSB0',
    'baudrate': 115200,
    'bytesize': serial.EIGHTBITS,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE
}


def crc16(data):
    """
    Calculate the CRC16 checksum of the given data.

    :param data: Bytes to calculate CRC16 on.
    :return: Calculated CRC16 checksum as an integer.
    """
    crc = 0xFFFF
    polynomial = 0xA001
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)
    return crc & 0xFFFF


def convert_to_utc(timestamp_str):
    """
    Convert a timestamp string to a UTC timestamp.

    :param timestamp_str: Timestamp string in the format 'YYMMDDhhmmssX'.
    :return: UTC timestamp as a float.
    """
    timestamp = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S%S')
    utc_timestamp = timestamp.replace(tzinfo=timezone.utc).timestamp()
    return utc_timestamp


def read_telegram():
    """
    Read a telegram from a serial port and return it along with CRC code.

    :return: Tuple containing the telegram as bytes and CRC code as bytes.
    """
    # Open a serial connection with the given port and baudrate
    ser = serial.Serial(**SERIAL_CONFIG)
    # Initialize an empty byte array to store the telegram
    telegram = bytearray()
    # Loop until a complete telegram is received
    while True:
        # Read one byte from the serial port
        byte = ser.read()
        # Extend the byte array with the byte
        telegram.extend(byte)
        # If the telegram starts with b"/", reset the telegram
        if byte == b"/" and len(telegram) > 1:
            telegram = bytearray(b"/")
        # If the telegram ends with b"!", return the telegram with those bytes
        if byte == b"!":
            crc_code = ser.read(4)
            return telegram, crc_code


def parse_telegram(message):
    """
    Parse a telegram message and extract information from it.

    :param message: Telegram message as a string.
    :return: Dictionary containing parsed information from the telegram.
    """
    parsed_telegram = {}
    for line in message.split("\n"):
        if line.startswith("/"):
            parsed_telegram["header"] = line[1:]
        else:
            try:
                idx = line.index("(")
                obis_code = line[:idx]
                value = line[idx:].replace("(", " (").split()
                if obis_code in obiscodes:
                    if len(value) > 1:
                        if obis_code == "1-0:1.6.0":
                            parsed_telegram["timestamp_piekvermogen"] = value[0]
                            parsed_telegram["piekvermogen_huidige_maand"] = value[1]
                        elif obis_code == "0-1:24.2.3":
                            parsed_telegram["timestamp_gas"] = value[0]
                            parsed_telegram["gas_verbruik_m³"] = value[1]
                    else:
                        parsed_telegram[obiscodes[obis_code]] = value
            except:
                continue
    return parsed_telegram


def main():
    """
    Main function to read and parse telegrams continuously.
    """
    telegram = {}
    while True:
        data, crc1 = read_telegram()
        message = parse_telegram(data.decode('utf-8'))
        print(telegram)
        print("\n")


if __name__ == "__main__":
    main()

