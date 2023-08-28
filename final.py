import binascii
import serial
import crcmod
import crcmod.predefined
import binascii


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
    crc16_ibm2 = crcmod.mkCrcFun(0x18005, initCrc=0, xorOut=0)
    crc16_ibm = crcmod.predefined.mkPredefinedCrcFun('crc16')
    # Convert the bytearray object to a bytes object
    telegram = bytes(telegram)
    # Calculate the CRC16 IBM checksum using the crc16_ibm function
    checksum = crc16_ibm(telegram)
    checksum2 = crc16_ibm2(telegram)

    # Convert the checksum to a hexadecimal string with four digits
    checksum_hex = f"{checksum:04x}"
    checksum_hex2 = f"{checksum2:04x}"
    # Compare the checksum with the CRC code in the telegram
    if checksum_hex == crc_code:
        print("The telegram is valid")
    else:
        print("The telegram is invalid")
        print("checksum : ", checksum_hex)
        print("checksum2 : ", checksum_hex2)
        print(crc_code)


# Import binascii module for crc16 calculation
# Define a function to decode a P1 frame

def decode_p1(frame):
    # Split the frame by line terminations
    lines = frame.split("\r\n")
    # Check if the first line starts with a slash and has a manufacturer FLAG id and a meter type
    if lines[0].startswith("/") and len(lines[0]) >= 5:
        flag_id = lines[0][1:4]
        meter_type = lines[0][5:]
        print(f"Manufacturer FLAG id: {flag_id}")
        print(f"Meter type: {meter_type}")
    else:
        print("Invalid first line")
        return
    # Check if the second line is empty
    if lines[1] == "":
        print("Empty second line")
    else:
        print("Invalid second line")
        return
    # Loop through the subsequent lines until the last line
    for line in lines[2:-1]:
        # Decode the COSEM objects using your own logic
        # For example, you can split the line by brackets and parse the values
        cosem_object = line.split("(")
        print(f"COSEM object: {cosem_object}")
    # Check if the last line starts with an exclamation mark and has a crc16 value
    if lines[-1].startswith("!") and len(lines[-1]) == 5:
        crc16 = lines[-1][1:]
        print(f"CRC16: {crc16}")
        # Calculate the crc16 of the whole frame including the "!" using IBM polynomial and initial value
        crc16_calculated = hex(binascii.crc_hqx(frame.encode(), 0))[2:].upper()
        print(f"CRC16 calculated: {crc16_calculated}")
        # Compare the crc16 values and check if they match
        if crc16 == crc16_calculated:
            print("CRC16 match")
        else:
            print("CRC16 mismatch")
    else:
        print("Invalid last line")
        return


def main():
    # config for serial comm.
    port = "/dev/ttyUSB0"
    baudrate = 115200
    while True:
        # read telegram
        p1_telegram, p1_crc16 = read_telegram(port, baudrate)
        # print data
        print(p1_telegram.decode("ascii"))
        crc16(p1_telegram, p1_crc16)
        decode_p1(p1_telegram.decode('ascii'))


if __name__ == "__main__":
    main()
