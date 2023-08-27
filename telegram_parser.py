import serial
import binascii

def crc16(data):
    """Calculates the CRC-16 of the given data."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for i in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xEDB88320
            else:
                crc >>= 1
    return crc

def checkcrc(telegram):
    """Checks the CRC code of the given telegram."""
    expected_crc = binascii.unhexlify(telegram[-2:])
    calculated_crc = crc16(telegram[:-2])

    if calculated_crc == expected_crc:
        return True
    else:
        return False

def parse_telegram(telegram):
    """Parses the given telegram and returns the data."""
    data = telegram[:-2]

    return data

def main():
    # Create a configuration dictionary
    config = {
        'port': '/dev/ttyUSB0',
        'baudrate': 115200,
        'bytesize': serial.EIGHTBITS,
        'parity': serial.PARITY_NONE,
        'stopbits': serial.STOPBITS_ONE
    }
    
    with serial.Serial(**config) as ser:
        while True:
            telegram = bytearray()
            
            # read data
            p1_line = ser.readline()
            
            # if new telegram reinitialize telegram object
            if "/" in p1_line.decode('ascii'):
                telegram = bytearray()
            
            telegram.extend(p1_line)
            
            if p1_line.decode('ascii').startswith('!'):
                # telegram complete (end of telegram is the crc code exampl: "!hex code")
                if checkcrc(telegram):
                    data = parse_telegram(telegram)
                    print(data)
                else:
                    print("CRC error")

if __name__ == "__main__":
    main()
