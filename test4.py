import serial

def crc_remainder(input_bitstring, polynomial_bitstring, initial_filler):
    """Calculate the CRC remainder of a string of bits using a chosen polynomial.
    initial_filler should be '1' or '0'.
    """
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = (len(polynomial_bitstring) - 1) * initial_filler
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] \
            = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
    return ''.join(input_padded_array)[len_input:]

def crc_check(input_bitstring, polynomial_bitstring, check_value):
    """Calculate the CRC check of a string of bits using a chosen polynomial."""
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = check_value
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] \
            = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
    return ('1' not in ''.join(input_padded_array)[len_input:])

# Define the CRC-16 IBM polynomial
IBM_POLYNOMIAL = "11000000000000101"

def calculate_crc16_IBM(telegram):
    # Convert the telegram to a bitstring
    telegram_bitstring = ''.join(format(byte, '08b') for byte in telegram)
    
    # Calculate the CRC-16 IBM value using the provided function
    calculated_crc = crc_remainder(telegram_bitstring, IBM_POLYNOMIAL, '0')
    
    # Convert the calculated CRC to an integer
    calculated_crc_int = int(calculated_crc, 2)
    
    return calculated_crc_int

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
            
            # Calculate the CRC-16 IBM of the telegram
            calculated_crc16 = calculate_crc16_IBM(telegram)
            
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
