import serial

ser = serial.Serial('/dev/tty.usbserial-1430', baudrate=115200, timeout=10)

if True:
  print('ahhhhh shit')
  msg = ser.readline()
  msg = msg.decode('utf-8')
  print('from serial:' + msg) 