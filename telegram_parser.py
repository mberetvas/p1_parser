import serial

def crc16(data):
    pass

def checkcrc(telegram):
    pass


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
                data = parse_telegram(telegram)
                print(data)
                # telegram complete (end of telegram is the crc code exampl: "!hex code")
                if checkcrc(telegram):
                    data = parse_telegram(telegram)
                    print(data)

                else:
                    print("CRC error")

if __name__ == "__main__":
    main()
