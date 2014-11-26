#!/usr/bin/env python
# encoding: utf-8
import SocketServer
import socket
from hashlib import sha1
from random import randint
from struct import unpack
from socket import inet_ntoa
from threading import Timer, Thread
import time

from bencode import bencode, bdecode

BOOTSTRAP_NODES = [
    ("router.bittorrent.com", 6881),
    ("dht.transmissionbt.com", 6881),
    ("router.utorrent.com", 6881)
]

def timer(t, f):
    Timer(t, f).start()

class DHTServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    def __init__(self, nid, host_address, handler_cls):
        SocketServer.UDPServer.__init__(self, host_address, handler_cls)
        self.rt = RTable()
        self.nid = nid

class DHTHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        req = self.request[0].strip()
        msg = bdecode(req)
        try:
            if msg["y"] == "r":
                if "nodes" in msg["r"]:
                    self.handle_fn_resp(msg)

            elif msg["y"] == "q":
                elif msg["q"] == "ping":
                    self.handle_ping_req(msg)
                if msg["q"] == "find_node":
                    self.handle_fn_req(msg)
                elif msg["q"] == "get_peers":
                    self.handle_gp_req(msg)
                elif msg["q"] == "announce_peer":
                    self.handle_ap_req(msg)
        except KeyError:
            pass

    def handle_fn_resp(self, msg):
        resp = msg["r"]
        if(resp and resp['nodes']):
            nodes = decode_nodes(resp['nodes'])
            for nid, ip, port in nodes:
                self.server.put(Node(nid, ip, port))

    def handle_ping_req(self, msg):
        resp = dict()
        resp['t'] = msg['t']
        resp['y'] = 'r'
        resp['r'] = {'id': self.server.nid}
        self.server.rt.update(Node(resp['id'], *self.client_address))
        self._sendmsg(resp)

    def handle_fn_req(self, msg):
        resp = dict()
        resp['t'] = msg['t']
        resp['y'] = 'r'
        resp['r'] = {'id': self.server.nid,
                     "nodes": encode_nodes([self.server.rt.get_rand()])
                    }
        self.server.rt.update(Node(resp['id'], *self.client_address))
        self._sendmsg(resp)

    def handle_gp_req(self, msg):
        resp = dict()
        resp['t'] = msg['t']
        resp['y'] = 'r'
        resp['r'] = {'id': self.server.nid,
                     "nodes": encode_nodes([self.server.rt.get_rand()]),
                     "token": random_id(4)
                    }
        self.server.rt.update(Node(resp['id'], *self.client_address))
        self._sendmsg(resp)

    def handle_ap_req(self, msg):
        with open("hashinfo", "a") as f:
            f.wirte("%s %s %s", msg['info_hash'], msg['port'], self.client_address[0])
        resp = dict()
        resp['t'] = msg['t']
        resp['y'] = 'r'
        resp['r'] = {'id': self.server.nid}
        self.server.rt.update(Node(resp['id'], *self.client_address))
        self._sendmsg(resp)

    def _sendmsg(self, msg):
        if not msg['t']:
            msg["t"] = random_trans_id()
        msg = bencode(msg)
        self.server.socket.sendto(msg, self.client_address)

class RTable():

    def __init__(self):
        self.nodes = set()

    def put(self, node):
        self.nodes.add(node)

    def get_rand(self):
        l = len(self.nodes)
        if(l > 0):
            return self.nodes[randint(0, l-1)]

    def update(self, node):
        for n in self.nodes:
            if n.nid == node.nid:
                n.beat = time.time()
                break
        else:
            self.put(node)


class Node(object):

    def __init__(self, nid, ip=None, port=None):
        self.nid = nid
        self.ip = ip
        self.port = port
        self.beat = time.time()

    def __eq__(self, node):
        return node.nid == self.nid

    def __hash__(self):
        return hash(self.nid)


class DHTSpy():
    def __init__(self, address):
        self.nid = random_id()
        self.address = address

    def start_server(self):
        self.server = DHTServer(self.nid, self.address, DHTHandler)
        self.server = threading.Thread(target=server.serve_forever)
        self.server.daemon = True

    def keepalive(self):
        


if __name__ == "__main__":
    # max_node_qsize bigger, bandwith bigger, spped higher
    dht = DHT(Master(), "0.0.0.0", 6881, max_node_qsize=20)
    dht.start()
    dht.wander()
