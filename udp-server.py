import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.bind(('', 6881))

while True:
    try:
        (data, address) = s.recvfrom(65536)
        print data
        print address
    except Exception:
        pass












