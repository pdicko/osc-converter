import sliplib

from pythonosc.osc_message_builder import OscMessageBuilder

SERVER_IP = "10.101.90.102"
PORT = 3032
ADDRESS = (SERVER_IP, PORT)

socket = sliplib.SlipSocket.create_connection(ADDRESS)
print(f"Connected to console at {socket.getpeername()}")

msg = OscMessageBuilder("/eos/ping")
msg.add_arg("hello console")
msg.add_arg(12)

# while True:
#     packet = msg.build().dgram
#     socket.send_msg(packet)
#     reply_bytes = socket.recv_msg()
#     reply = reply_bytes.decode()
#     print(f"Console: {reply}")

packet = msg.build().dgram
socket.send_msg(packet)

while True:
    reply_bytes = socket.recv_msg()
    reply = reply_bytes.decode()
    print(f"Console: {reply_bytes}")
