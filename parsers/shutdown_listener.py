from sliplib import Driver
from osc4py3 import oscbuildparse

def sys_shutdown_request(data):
  d = Driver()
  messages = d.receive(data)
  for msg in messages:
      osc_msg = oscbuildparse.decode_packet(msg)
      addrpattern = osc_msg.addrpattern
      if addrpattern == '/bridge/shutdown':
        return True
      else:
        return False
      

