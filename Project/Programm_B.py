import argparse
import base64
import binascii
import socket
import struct

# 1. Empfang der von Programm A gesendeten Daten vom Netzwerkstack.
def receive_data():
    icmp = socket.getprotobyname('icmp')
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

    print('ICMP listener started')
    print('listening ...\n')

    while True:
        packet, _ = sock.recvfrom(65565)
        # IP header is the first 20 bytes of the packet
        ip_header = packet[:20]
        # ICMP packet is in the IP packet's data
        icmp_packet = packet[20:]
        # ICMP header is in the first 8 bytes of the ICMP packet
        type, code, checksum, identifier, sequence_number = struct.unpack('bbHHh', icmp_packet[:8])
        if type == 8:  # Echo Request
            # Decoding the data
            encoded_data = icmp_packet[8:]
            try:
                data = base64.b64decode(encoded_data).decode()
                # Displaying the decoded data on the screen
                print(f"Incomming Message >>\n{data}")
                print("<< End of Message")
            except Exception as e:
                print(f"error: {e}")

def main():
    receive_data()

if __name__ == "__main__":
    main()
