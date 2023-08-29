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


# def crc16(telegram, crc_code):
#     # Define the CRC16 IBM function with polynomial 0x18005 and initial value 0;
#     crc16_ibm2 = crcmod.mkCrcFun(0x18005, initCrc=0, xorOut=0)
#     crc16_ibm = crcmod.predefined.mkPredefinedCrcFun('crc-16-maxim')
#     crc = crcmod.mkCrcFun(0x1A001, initCrc=0, xorOut=0)
#     # Convert the bytearray object to a bytes object
#     telegram = bytes(telegram)
#     # Calculate the CRC16 IBM checksum using the crc16_ibm function
#     checksum = crc16_ibm(telegram)
#     checksum2 = crc16_ibm2(telegram)
#     checksum3 = crc(telegram)

#     # Convert the checksum to a hexadecimal string with four digits
#     checksum_hex = f"{checksum:04x}"
#     checksum_hex2 = f"{checksum2:04x}"
#     checksum3_hex = f"{checksum3:04x}"
#     # Compare the checksum with the CRC code in the telegram
#     if checksum_hex == crc_code:
#         print("The telegram is valid")
#     else:
#         print("The telegram is invalid")
#         print("checksum : ", checksum_hex)
#         print("checksum2 : ", checksum_hex2)
#         print("checksum3 : ", checksum3_hex)
#         print(crc_code)


# def crc16(telegram):
#     """
#     Calculate the CRC16 value for the given telegram
#     :param str telegram:
#     """
#     crcValue = 0x0000
#     if len(TelegramParser.crc16_tab) == 0:
#         for i in range(0, 256):
#             crc = c_ushort(i).value
#             for j in range(0, 8):
#                 if crc & 0x0001:
#                     crc = c_ushort(crc >> 1).value ^ 0xA001
#                 else:
#                     crc = c_ushort(crc >> 1).value
#             TelegramParser.crc16_tab.append(hex(crc))
#     for c in telegram:
#         d = ord(c)
#         tmp = crcValue ^ d
#         rotated = c_ushort(crcValue >> 8).value
#         crcValue = rotated ^ int(
#             TelegramParser.crc16_tab[(tmp & 0x00FF)], 0)
#     return crcValue

def crc16(telegram):
    """
    Calculate the CRC16 value for the given telegram
    :param str telegram:
    """
    crcValue = 0x0000
    crc16_tab = []
    if len(crc16_tab) == 0:
        for i in range(0, 256):
            crc = i
            for j in range(0, 8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc = crc >> 1
            crc16_tab.append(hex(crc))
    for c in telegram:
        d = ord(c)
        tmp = crcValue ^ d
        rotated = crcValue >> 8
        crcValue = rotated ^ int(crc16_tab[(tmp & 0x00FF)], 0)
    return crcValue

# def crc16(data: bytes, poly=0x8408):
#     data = bytearray(data)
#     crc = 0xFFFF
#     for b in data:
#         cur_byte = 0xFF & b
#         for _ in range(0, 8):
#             if (crc & 0x0001) ^ (cur_byte & 0x0001):
#                 crc = (crc >> 1) ^ poly
#             else:
#                 crc >>= 1
#             cur_byte >>= 1
#     crc = (~crc & 0xFFFF)
#     crc = (crc << 8) | ((crc >> 8) & 0xFF)
#     return crc & 0xFFFF


def main():
    # config for serial comm.
    port = "/dev/ttyUSB0"
    baudrate = 115200
    while True:
        # read telegram
        p1_telegram, p1_crc16 = read_telegram(port, baudrate)
        # print data
        print(p1_telegram.decode("ascii"))
        print(f"\n{p1_crc16}")
        print(crc16(p1_telegram.decode("ascii")))


if __name__ == "__main__":
    main()
