import serial
import crcmod


# serial port config dictionary
SERIAL_CONFIG = {
    'port': '/dev/ttyUSB0',
    'baudrate': 115200,
    'bytesize': serial.EIGHTBITS,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE
}


def crc16(data):
    # Create a crc function with x16+x15+x2+1 and least significant bit firts
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    # compute the crc16 value of the data message
    calc_crc16 = crc16(data.encode())
    # convert the crc16 value to a 4-digit hexadecimal string with MSB first
    crc16_hex = format(calc_crc16, "04X")
    print("calculated crc16:", crc16_hex)
    return crc16_hex

# read data from the serial port


def read_telegram():
    # define the serial port
    ser = serial.Serial(**SERIAL_CONFIG)
    lines = []
    while True:
        line = ser.readline.decode().strip()
        if line.startswith("/"):
            lines = []
        lines.append(line)
        if line.startswith("!"):
            # process the complete set of lines
            data = "\n".join(lines)
    return data


def main():
    data = read_telegram()
    print(data)
    crc16(data)


if __name__ == "__main__":
    main()
