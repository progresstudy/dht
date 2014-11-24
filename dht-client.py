import socket
from hashlib import sha1
from random import randint
from struct import unpack
from socket import inet_ntoa
from threading import Timer, Thread
from time import sleep
from bencode import bencode, bdecode

address=[
            ("router.bittorrent.com", 6881),
            ("dht.transmissionbt.com", 6881),
            ("router.utorrent.com", 6881)
        ]
TID_LENGTH = 4
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

def entropy(length):
    return ''.join(chr(randint(0, 255)) for _ in xrange(length))


def random_id():
    hash = sha1()
    hash.update(entropy(20))
    return hash.digest()

def send_krpc(msg, address):
    global s
    try:
        s.sendto(bencode(msg), address)
    except Exception:
        pass

def send_find_node(address, nid=None):
    tid = entropy(TID_LENGTH)
    msg = dict(
        t=tid,
        y="q",
        q="find_node",
        a=dict(id=nid, target=random_id())
    )
    print msg
    send_krpc(msg, address)

def send_ping(address, nid=None):
    tid = entropy(TID_LENGTH)
    msg = dict(
        t=tid,
        y="q",
        q="ping",
        a=dict(id=nid)
    )
    print msg
    print address
    send_krpc(msg, address)

if __name__ == "__main__":
    nid = random_id()
    for a in address:
        #send_find_node(a, nid)
        send_ping(a, nid)
