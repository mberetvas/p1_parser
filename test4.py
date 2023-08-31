import serial
import crcmod.predefined

def read_telegram(port, baudrate):
    # Create a CRC16 object with the same parameters as in the telegram
    crc_func = crcmod.predefined.mkCrcFun('crc-16')
    
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
        # If the telegram ends with b"!", calculate the CRC16
        if byte == b"!":
            # Remove the "!" from the telegram
            telegram = telegram[:-1]
            # Calculate the CRC16 of the telegram
            calculated_crc16 = crc_func(telegram)
            
            # Read the CRC code from the telegram
            crc_code = ser.read(4).decode("ascii")
            
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
