import base64
from scapy.all import sniff, ICMP

# 1. Empfang der von Programm A gesendeten Daten vom Netzwerkstack.
def process_packet(packet):
    if packet.haslayer(ICMP):
        # 2. Nur ICMP Requests (Typ 8) werden berücksichtigt. ICPM Replies (Typ 0) wird ignoriert.
        if packet[ICMP].type != 8: return
        # 3. Decodierung der Daten (Umwandlung in Text).
        encoded_data = packet[ICMP].load
        data = decode_data(encoded_data)
        # 4. Ausgabe der decodierten Daten auf dem Bildschirm.
        print(data)

# Decodierung der Daten
def decode_data(encoded_data):
    decoded_data = base64.b64decode(encoded_data).decode()
    return decoded_data

# Hauptfunktion
def main():
    sniff(filter="icmp and host destination_ip", prn=process_packet)

if __name__ == "__main__":
    main()
