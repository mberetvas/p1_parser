import serial

def crc16(data):
    pass

def checkcrc(telegram):
    pass


def parse_telegram(telegram):
    pass

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
            decoded_p1 = p1_line.decode('ascii')

            # check begginning of telegram
            if "/" in decoded_p1:
                telegram = bytearray()
            telegram = telegram.extend(p1_line)
            print("\n")
            print(telegram)

if __name__ == "__main__":
    main()
