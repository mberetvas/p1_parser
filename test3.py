import serial
import binascii

CRC16_POLY = 0xA001

def crc16(data):
    """Calculates the CRC-16 of the given data."""
    print(data,"\n")
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= CRC16_POLY
            else:
                crc >>= 1
    return crc & 0xFFFF

def check_crc(telegram):
    """Checks the CRC code of the given telegram."""
    try:
        if len(telegram) < 2:
            return False

        exclamation_index = telegram.find(b'!')
        
        if exclamation_index != -1 and exclamation_index + 5 <= len(telegram):
            expected_crc = binascii.unhexlify(telegram[exclamation_index + 1:exclamation_index + 5])
            calculated_crc = crc16(telegram[:exclamation_index + 1])
            print("expected crc: ", expected_crc)
            print("calculated crc: ", calculated_crc)
            
            if calculated_crc == int.from_bytes(expected_crc, byteorder='big'):
                return True
        return False
    except Exception as e:
        print(f"Error in check_crc(telegram): {e}")
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
        telegram = bytearray()
        
        while True:
            p1_line = ser.readline()
            telegram.extend(p1_line)
            
            if "/" in p1_line.decode('ascii'):
                telegram = bytearray()
            

            if check_crc(telegram):
                data = parse_telegram(telegram)
                print(data)
            else:
                print("CRC error")

if __name__ == "__main__":
    main()
