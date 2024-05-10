"""

Streaming Process: Uses port 9999

Create a stream of data using 1 year of Tesla Stock price from Yahoo Finance
Link: https://finance.yahoo.com/quote/TSLA

Reverse the order of the rows to read OLDEST data first.

We'll stream forever - or until we read the end of the file. 
Use use Ctrl-C to stop. (Hit Control key and c key at the same time.)

Explore more at 
https://wiki.python.org/moin/UdpCommunication

"""

# Import from Python Standard Library
import csv
import socket
import time
import logging

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Declare program constants (typically constants are named with ALL_CAPS)
HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "tsla.csv"
OUTPUT_FILE_NAME = "out9.txt"

# Custom function to prepare the message from row
# Utilize CSV values from intput_file_name
def prepare_message_from_row(row):
    """Prepare a binary message from a given row."""
    Date, Open, High, Low, Close, AdjClose, Volume = row
    fstring_message = f"[{Date}, {Open}, {High}, {Low}, {Close}, {AdjClose}, {Volume}]"
    MESSAGE = fstring_message.encode()
    logging.debug(f"Prepared message: {fstring_message}")
    return MESSAGE

# Custom function for reading from input_file_name
# Writing messages to address_tuple
# Writing rows to output_file_name
def stream_row(input_file_name, address_tuple, output_file_name):
    logging.info(f"Starting to stream data from {input_file_name} to {address_tuple}.")
    with open(input_file_name, "r") as input_file, open(output_file_name, "w", newline='') as output_file:
        logging.info(f"Opened for reading: {input_file_name}.")
        reader = csv.reader(input_file, delimiter=",")        
        header = next(reader)  # Skip header row
        logging.info(f"Skipped header row: {header}")
        output_file.write('|'.join(header) + '\n')

        # Use socket enumerated types to configure our socket object
        # Set our address family to (IPV4) for 'internet'
        # Set our socket type to UDP (datagram)
        ADDRESS_FAMILY = socket.AF_INET 
        SOCKET_TYPE = socket.SOCK_DGRAM 

        # Call the socket constructor, socket.socket()
        # A constructor is a special method with the same name as the class
        # Use the constructor to make a socket object
        # and assign it to a variable named `sock_object`
        sock_object = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)
        
        # Write stream messages to the console
        # Write to the output file and wait 1 second per steam
        for row in reader:
            MESSAGE = prepare_message_from_row(row)
            sock_object.sendto(MESSAGE, address_tuple)
            output_file.write('|'.join(row) + '\n')
            logging.info(f"Sent: {MESSAGE} on port {PORT}. Hit CTRL-c to stop.")
            time.sleep(1) # wait 3 seconds between messages

# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        logging.info("===============================================")
        logging.info("Starting Stock Price Streaming Process.")
        stream_row(INPUT_FILE_NAME, ADDRESS_TUPLE, OUTPUT_FILE_NAME)
        logging.info("Streaming complete!")
        logging.info("===============================================")
    except Exception as e:
        logging.error(f"An error occurred: {e}")