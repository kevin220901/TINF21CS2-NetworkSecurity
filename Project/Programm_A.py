# Programm_A.py
import argparse
import socket
import struct
import base64
import sys


def read_from_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def calculate_checksum(source_string):
    count_to = (int(len(source_string) / 2)) * 2
    sum = 0
    count = 0

    # Handle bytes in pairs (decoding as short ints)
    lo_byte = 0
    hi_byte = 0
    while count < count_to:
        if (sys.byteorder == "little"):
            lo_byte = source_string[count]
            hi_byte = source_string[count + 1]
        else:
            lo_byte = source_string[count + 1]
            hi_byte = source_string[count]
        sum = sum + (hi_byte * 256 + lo_byte)
        count += 2

    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should not be relevant in this case
    if count_to < len(source_string): # Check for odd length
        lo_byte = source_string[len(source_string) - 1]
        sum += lo_byte

    sum &= 0xffffffff  # Truncate sum to 32 bits (a variance from ping.c, which uses signed ints, but overflow is unlikely in ping)

    sum = (sum >> 16) + (sum & 0xffff)  # Fold 32-bit sum to 16 bits
    sum += (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff  # Keep lower 16 bits
    # Swap bytes. Bugger me if I know why. :P
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def send_data(encoded_data, destination_ip):
    icmp = socket.getprotobyname('icmp')
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

    # ICMP header fields
    type = 8  # Echo Request
    code = 0
    checksum = 0
    identifier = 0
    sequence_number = 0

    # Pack header fields into struct with checksum set to zero
    header = struct.pack('bbHHh', type, code, checksum, identifier, sequence_number)
    packet = header + encoded_data.encode()  # Packet is header + payload

    # Calculate checksum
    checksum = calculate_checksum(packet)
    header = struct.pack('bbHHh', type, code, socket.htons(checksum), identifier, sequence_number)
    packet = header + encoded_data.encode()

    sock.sendto(packet, (destination_ip, 1))  # ICMP uses port number 1
    print(f"Message sent to {destination_ip}")


def main(file_path, destination_ip):
    data = read_from_file(file_path)
    encoded_data = base64.b64encode(data.encode()).decode()
    send_data(encoded_data, destination_ip)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send data over ICMP.')
    parser.add_argument('file_path', help='Path to the text file')
    parser.add_argument('destination_ip', help='Destination IP address')
    args = parser.parse_args()

    main(args.file_path, args.destination_ip)
