import serial
import crcmod


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


def crc16(telegram, crc_code):
    # Define the CRC16 IBM function with polynomial 0x18005 and initial value 0;
    crc16_ibm = crcmod.mkCrcFun(0x18005, initCrc=0, xorOut=0)
    # Convert the bytearray object to a bytes object
    telegram = bytes(telegram)
    # Calculate the CRC16 IBM checksum using the crc16_ibm function
    checksum = crc16_ibm(telegram)
    # Convert the checksum to a hexadecimal string with four digits
    checksum_hex = f"{checksum:04x}"
    # Compare the checksum with the CRC code in the telegram
    if checksum_hex == crc_code:
        print("The telegram is valid")
    else:
        print("The telegram is invalid")
        print(checksum_hex)
        print(crc_code)


def main():
    # config for serial comm.
    port = "/dev/ttyUSB0"
    baudrate = 115200
    while True:
        # read telegram
        p1_telegram, p1_crc16 = read_telegram(port, baudrate)
        # print data
        print(p1_telegram)

        crc16(p1_telegram, p1_crc16)


if __name__ == "__main__":
    main()
