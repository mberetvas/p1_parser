import serial

# Define the CRC-16 IBM polynomial
IBM_POLYNOMIAL = 0x8005
IBM_POLY_reversed = 0xA001

def calculate_crc16(telegram):
    # Initialize the CRC-16 value with 0
    crc = 0
    for byte in telegram:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ IBM_POLY_reversed
            else:
                crc <<= 1
            crc &= 0xFFFF  # Ensure the result stays 16 bits
    
    return crc

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
        # If the telegram ends with b"!", read the CRC code
        if byte == b"!":
            crc_code = ser.read(4).decode("ascii")
            
            # Calculate the CRC-16 of the telegram using IBM polynomial
            calculated_crc16 = calculate_crc16(telegram)
            
            print(telegram.decode("ascii"))
            print(int(crc_code, 16)," = ",calculated_crc16)
            # Compare the calculated CRC with the received CRC
            if calculated_crc16 == int(crc_code, 16):
                print("CRC check passed.")
            else:
                print("CRC check failed.")
            
            # Return the telegram and CRC code
            return telegram, crc_code

def main():
    # config for serial comm.
    port = "/dev/ttyUSB0"
    baudrate = 115200
    while True:
        # read telegram.
        p1_telegram, p1_crc16 = read_telegram(port, baudrate)

if __name__ == "__main__":
    main()
