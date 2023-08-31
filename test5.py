import serial
import crcmod
import time


# serial port config dictionary
SERIAL_CONFIG = {
    'port': '/dev/ttyUSB0',
    'baudrate': 115200,
    'bytesize': serial.EIGHTBITS,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE
}


# def crc16(data):
#     # Create a crc function with x16+x15+x2+1 and least significant bit firts
#     crc16 = crcmod.mkCrcFun(0xA001, rev=True, initCrc=0xFFFF, xorOut=0x0000)
#     # compute the crc16 value of the data message
#     calc_crc16 = crc16(data.encode())
#     # convert the crc16 value to a 4-digit hexadecimal string with MSB first
#     crc16_hex = format(calc_crc16, "04X")
#     print("calculated crc16:", crc16_hex)
#     return crc16_hex

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


# def read_telegram():
#     # define the serial port
#     ser = serial.Serial(**SERIAL_CONFIG)
#     lines = []
#     while True:
#         line = ser.readline()
#         if line.decode("ascii").startswith("/"):
#             lines = []
#         lines.append(line.decode("ascii"))
#         if line.decode("ascii").startswith("!"):
#             # process the complete set of lines
#             data = "\n".join(lines)
#             break
#     return data

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
            return telegram, crc_code.decode("utf-8")


def main():
    while True:
        data = read_telegram()
        print(data[:-4])
        print(crc16(data[:-4]))
        # time.sleep(5)


if __name__ == "__main__":
    main()
