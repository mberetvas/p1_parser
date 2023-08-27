import serial


def crc16(data):
    crc = 0xFFFF
    polynomial = 0x1021

    for byte in data:
        for bit in range(8):
            if (crc & 0x01):
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1

            byte >>= 1

    return crc


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

            # read data
            p1_line = ser.readline()
            decoded_p1 = p1_line.decode('ascii')

            # check begginning of telegram
            if "/" in decoded_p1:
                telegram = bytearray()
            try:
                telegram.extend(p1_line)
            except:
                continue

            if "!" in decoded_p1:
                # print complete telegram
                print("\n")
                print(telegram)
                
                try:
                    print(hex(crc16(telegram)))
                except:
                    print("crc nok")


if __name__ == "__main__":
    main()
