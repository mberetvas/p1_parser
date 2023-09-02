import serial
import sqlite3
from datetime import datetime, timezone
import pytz


# Serial port configuration dictionary
SERIAL_CONFIG = {
    'port': '/dev/ttyUSB0',
    'baudrate': 115200,
    'bytesize': serial.EIGHTBITS,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE
}

# Define the path to the SQLite database file
DB_PATH = "p_db.db"

# Dict with obiscode description (24) to add or remove from database comment line out
obiscodes = {
    #"0-0:96.1.4":"verson_info",  # Versie informatie xxxyy waar xxx=dsmr p1 versie en yy=e-MUCs-h versie
    #"0-0:96.1.1":"equipment_id", # Hex encoded equip. id according to DIN 43863-5
    "0-0:1.0.0":"timestamp", # Timestamp YYMMDDhhmmssX X is S=Summer W=winter
    "1-0:1.8.1":"totaal_verbruik_dagtarief_kwh",
    "1-0:1.8.2":"totaal_verbruik_nachttarief_kwh",
    "1-0:2.8.1":"totaal_injectie_dagtarief_kwh",
    "1-0:2.8.2":"Totale_injectie_nachttarief_kwh",
    "0-0:96.14.0":"Tarief_indicatie", # tarief_indicatie
    "1-0:1.4.0":"gemmiddeld_verbruik_kw", # Gemmiddeld verbruik kw
    "1-0:1.6.0":"piekvermogen_huidige_maand", # Maximum piekvermogen voor huidige maand
    #"0-0:98.1.0":"piekvermogen _van_laatste_13_maanden",
    "1-0:1.7.0":"actief_verbruik_kw", # actief verbruik in kw
    "1-0:2.7.0":"actief_injectie_kw", # actieve injectie in kw
    "1-0:21.7.0":"instant_vermogen_L1+P_kw", # instantaneous active power L1 +P
    "1-0:22.7.0":"instant_vermogen_l1_injectie_kw", # instantaneous active power L1 -P
    "1-0:32.7.0":"spanning_V", # instantaneous voltage
    "1-0:31.7.0":"stroom_A", # instantaneous current
    #"0-0:96.3.10":"stand_zekering", # Breaker state 0=Disconnected 1=connected 3=ready for connection
    #"0-0:17.0.0":"Limiter_threshold_kw", # limiter_threshold
    #"1-0:31.4.0":"fuse_threshold_A", # fuse_treshold
    #"0-0:96.13.0":"Text_Messag", # (for future use)
    #"0-1:24.1.0":"Device_type", # device-type
    #"0-1:24.4.0":"gasklep_stand" # gasklep_stand
    "0-1:24.2.3":"gas_verbruik_m³" # Last value of 'not temperature corrected' gas volume in m³,including decimal values and capture time
}


def insert_telegram_data(parsed_telegram):
    """
    Insert parsed telegram data into an SQLite database.

    :param parsed_telegram: Dictionary containing parsed telegram data.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Prepare the SQL statement to insert data into the existing table
        insert_data_sql = '''
            INSERT INTO p1_data (
                timestamp,
                totaal_verbruik_dagtarief_kwh,
                totaal_verbruik_nachttarief_kwh,
                totaal_injectie_dagtarief_kwh,
                Totale_injectie_nachttarief_kwh,
                Tarief_indicatie,
                gemmiddeld_verbruik_kw,
                piekvermogen_huidige_maand,
                timestamp_piekvermogen,
                actief_verbruik_kw,
                actief_injectie_kw,
                instant_vermogen_L1_P_kw,
                instant_vermogen_L1_injectie_kw,
                spanning_V,
                stroom_A,
                gas_verbruik_m³,
                timestamp_gas
            )
            VALUES (
                :timestamp,
                :totaal_verbruik_dagtarief_kwh,
                :totaal_verbruik_nachttarief_kwh,
                :totaal_injectie_dagtarief_kwh,
                :Totale_injectie_nachttarief_kwh,
                :Tarief_indicatie,
                :gemmiddeld_verbruik_kw,
                :piekvermogen_huidige_maand,
                :timestamp_piekvermogen,
                :actief_verbruik_kw,
                :actief_injectie_kw,
                :instant_vermogen_L1_P_kw,
                :instant_vermogen_L1_injectie_kw,
                :spanning_V,
                :stroom_A,
                :gas_verbruik_m³,
                :timestamp_gas
            )
        '''
        
        # Convert timestamps to UTC timestamps (float) by accessing the first element of the list
        # parsed_telegram['timestamp'] = convert_to_utc(parsed_telegram['timestamp'][0])
        # parsed_telegram['timestamp_piekvermogen'] = convert_to_utc(parsed_telegram['timestamp_piekvermogen'][0])
        # parsed_telegram['timestamp_gas'] = convert_to_utc(parsed_telegram['timestamp_gas'][0])

        # Replace missing data with 0.
        # for key in parsed_telegram.keys():
        #     if key != "header":
        #         if key in parsed_telegram:
        #             parsed_telegram[key] = parsed_telegram[key]
        #         else:
        #             parsed_telegram[key] = 0.0

        cursor.execute(insert_data_sql, parsed_telegram)
        conn.commit()
    except Exception as e:
        print(f"Error inserting data into the database: {e}")
    finally:
        conn.close()


def print_database_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve all records from the table
        cursor.execute("SELECT * FROM p1_data")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Print the column headers
        column_names = [description[0] for description in cursor.description]
        print("\t".join(column_names))

        # Print the data
        for row in rows:
            print("\t".join(str(value) for value in row))

    except Exception as e:
        print(f"Error reading data from the database: {e}")
    finally:
        conn.close()

def crc16(data):
    """
    Calculate the CRC16 checksum of the given data.

    :param data: Bytes to calculate CRC16 on.
    :return: Calculated CRC16 checksum as an integer.
    """
    crc = 0xFFFF
    polynomial = 0xA001
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)
    return crc & 0xFFFF


def convert_to_utc(timestamp_str):
    """
    Convert a timestamp string to a UTC timestamp in the format 'YYYY-MM-DDTHH:MM:SSZ'.

    :param timestamp_str: Timestamp string in the format 'YYMMDDhhmmssX'.
    :return: UTC timestamp in the format 'YYYY-MM-DDTHH:MM:SSZ'.
    """
    # Remove "(" and ")"
    
    # Remove the 'S' or 'W' suffix from the timestamp string
    suffix = timestamp_str[-1]
    timestamp_str = timestamp_str.rstrip('SW')
    # Create a datetime object from the timestamp string
    local_datetime = datetime.strptime(timestamp_str, '%y%m%d%H%M%S')
    # Create a timezone object for the local timezone
    if suffix == 'S':
        local_tz = pytz.timezone('CET')
    elif suffix == 'W':
        local_tz = pytz.timezone('CET')  # Replace with the correct timezone for winter time
    else:
        raise ValueError("Invalid timestamp suffix: {}".format(suffix))
    # Set the timezone for the datetime object, taking into account DST rules
    local_datetime = local_tz.localize(local_datetime, is_dst=None)
    # Convert the datetime object to UTC and get the UTC timestamp as a float
    utc_datetime = local_datetime.astimezone(timezone.utc)
    utc_timestamp = utc_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    return utc_timestamp


def read_telegram():
    """
    Read a telegram from a serial port and return it along with CRC code.

    :return: Tuple containing the telegram as bytes and CRC code as bytes.
    """
    # Open a serial connection with the given port and baudrate
    ser = serial.Serial(**SERIAL_CONFIG)
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
            return telegram, crc_code


def parse_telegram(message):
    """
    Parse a telegram message and extract information from it.

    :param message: Telegram message as a string.
    :return: Dictionary containing parsed information from the telegram.
    """
    parsed_telegram = {}
    for line in message.split("\n"):
        if line.startswith("/"):
            parsed_telegram["header"] = line[1:]
        else:
            try:
                idx = line.index("(")
                obis_code = line[:idx]
                value = line[idx:].replace("(", " (").split()
                if obis_code in obiscodes:
                    if len(value) > 1:
                        if obis_code == "1-0:1.6.0":
                            parsed_telegram["timestamp_piekvermogen"] = value[0]
                            parsed_telegram["piekvermogen_huidige_maand"] = value[1]

                        elif obis_code == "0-1:24.2.3":
                            parsed_telegram["timestamp_gas"] = value[0]
                            parsed_telegram["gas_verbruik_m³"] = value[1]
                    else:
                        parsed_telegram[obiscodes[obis_code]] = value
            except:
                continue
    return parsed_telegram


def main():
    """
    Main function to read and parse telegrams continuously.
    """
    n = 0
    while True:
        n += 1
        data, crc1 = read_telegram()
        parsed_telegram = parse_telegram(data.decode('utf-8'))
        try:
            timestamp = parsed_telegram["timestamp"]
            #print(timestamp)
            
            timestamp = timestamp.strip('()')
            print(timestamp)


            #  print(convert_to_utc(timestamp))
        except Exception as e:
            print(e)
        # for k,v in parsed_telegram.items():
        #     print(f"{k} = {v}")
        print("\n")
        # insert_telegram_data(parsed_telegram)
        # if n == 10:
        #     print_database_data()




if __name__ == "__main__":
    main()

