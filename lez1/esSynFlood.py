from scapy.all import *

# Application layer

target = "192.168.1.1"
tport = 90

#TCP layer
tcp = TCP(sport = 12, dport = tport, flags="S")

#IP layer
ip = IP(dst = target)

#Payload
payload = Raw(b'payload laboratorio di rete')

pack = ip/tcp/payload
#due modi
# ciclo
# while True:
#     send(pack, verbose=1)
# oppure uso loop = 1, va avanti fino a quando non riceve un CTRL+C
send(pack, loop=1)