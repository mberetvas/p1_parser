import binascii
import serial
import crcmod
import crcmod.predefined
import binascii
from ctypes import c_ushort


def read_telegram(port, baudrate):
    # Open a serial connection with the given port and baudrate
    ser = serial.Serial(port, baudrate)
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



def main():
    # config for serial comm.
    port = "/dev/ttyUSB0"
    baudrate = 115200
    while True:
        # read telegram.
        p1_telegram, p1_crc16 = read_telegram(port, baudrate)


if __name__ == "__main__":
    main()
