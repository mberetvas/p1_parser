import serial
import crcmod
import time
import re
import pandas


# serial port config dictionary
SERIAL_CONFIG = {
    'port': '/dev/ttyUSB0',
    'baudrate': 115200,
    'bytesize': serial.EIGHTBITS,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE
}


def crc16(data):
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


def read_telegram():
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
    # Extract the information from each line of the message
    parsed_telegram = {}
    for line in message.split("\n"):
        if line.startswith("/"):
            parsed_telegram["header"] = line[1:]
        else:
            # pattern = r"(\d+-\d+:\d+\.\d+\.\d+)\((\d+\.\d+)\*(\w+)\)"
            # match = re.match(pattern, line)
            # if match:
            #     key = match.group(1)
            #     value = match.group(2)
            #     unit = match.group(3)
            #     parsed_telegram[key] = value,unit
            idx = line.index(":")
            first_part = line[:idx]
            second_part = line[idx:]
            print(f"{first_part} = {second_part}")
    return parsed_telegram

def main():
    while True:
        data, crc1 = read_telegram()
        message = parse_telegram(data.decode('utf-8'))

        print('\n')

if __name__ == "__main__":
    main()
