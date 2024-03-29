import binascii
import serial
import crcmod
import crcmod.predefined
import binascii
from ctypes import c_ushort


# serial port config dictionary
SERIAL_CONFIG = {
    'port': '/dev/ttyUSB0',
    'baudrate': 115200,
    'bytesize': serial.EIGHTBITS,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE
}

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
            return telegram, crc_code.decode("ascii")

def crc16(data):
    # Create a crc function with x16+x15+x2+1 and least significant bit firts
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    # compute the crc16 value of the data message
    calc_crc16 = crc16(data.encode())
    # convert the crc16 value to a 4-digit hexadecimal string with MSB first
    crc16_hex = format(calc_crc16, "04X")
    print("calculated crc16:", crc16_hex)
    return crc16_hex


def main():

    while True:
        # read telegram.
        p1_telegram, p1_crc16 = read_telegram()


if __name__ == "__main__":
    main()
