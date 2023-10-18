import sliplib

from osc4py3 import oscbuildparse


SERVER_IP = "10.101.90.102"
PORT = 3032
ADDRESS = (SERVER_IP, PORT)

socket = sliplib.SlipSocket.create_connection(ADDRESS)
print(f"Connected to console at {socket.getpeername()}")

msg = oscbuildparse.OSCMessage("/eos/ping", ",si", ("hello console", 12))
packet = oscbuildparse.encode_packet(msg)
socket.send_msg(packet)
print(msg)

while True:
    reply_bytes = socket.recv_msg()
    reply = oscbuildparse.decode_packet(reply_bytes)
    print(reply)
