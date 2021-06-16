#pip3 install scapy


from scapy.all import *

# Application layer
target = "192.168.1.128"
tport = 90

#TCP layer
tcp = TCP(sport = 12, dport = tport, flags="S")

#IP layer
ip = IP(dst = target)

#Payload
payload = Raw(b'payload laboratorio di rete')

pack = ip/tcp/payload
send(pack, verbose=1)
