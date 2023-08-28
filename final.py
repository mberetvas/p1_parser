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
        # If the telegram ends with b"!" and has four bytes after it, return the telegram with those bytes
        if byte == b"!" and ser.in_waiting == 2:
            crc_code = ser.read(2)
            return telegram + crc_code


def crc16():
    # Define the CRC16 IBM function with polynomial 0x8005 and initial value 0
    crc16_ibm = crcmod.mkCrcFun(0x8005, initCrc=0, xorOut=0)
    # Assume that you have read the telegram as a bytes object
    telegram = b"/...!"
    # Calculate the CRC16 IBM checksum using the crc16_ibm function
    checksum = crc16_ibm(telegram)
    # Convert the checksum to a hexadecimal string with four digits
    checksum_hex = f"{checksum:04x}"
    # Extract the CRC code from the last line of the telegram
    crc_code = telegram[-4:-1].decode("ascii")
    # Compare the checksum with the CRC code in the telegram
    if checksum_hex == crc_code:
        print("The telegram is valid")
    else:
        print("The telegram is invalid")


def main():
    # config for serial comm.
    port = "/dev/ttyUSB0"
    baudrate = 115200
    # read telegram
    p1_telegram, p1_crc16 = read_telegram(port, baudrate)
    # print data
    print(p1_telegram)
    print(p1_crc16, "\n")


if __name__ == "__main__":
    main()
