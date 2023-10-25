import serial
import sliplib

from sliplib import slip
from osc4py3 import oscbuildparse

DEVICE = "/dev/tty.usbserial-1430"
BAUDRATE = 115200

serial = serial.Serial(DEVICE, BAUDRATE, timeout=0.1)
print("Opening serial port...")

driver = slip.Driver()

while True:
    data = serial.readline()
    if data:
        msg_list = driver.receive(data)
        for msg in msg_list[1:]:
            print(oscbuildparse.decode_packet(msg))
