import sys
import socket
# import serial
import serial.threaded
import time

from config.config import get_current_settings


class SerialToNet(serial.threaded.Protocol):
    """serial->socket"""

    def __init__(self):
        self.socket = None

    def __call__(self):
        return self

    def data_received(self, data):
        if self.socket is not None:
            self.socket.sendall(data)


def open_bridge(serial_conn, socket_address):
    ser = serial_conn
    # current_device_settings = get_current_settings('DEVICE-CURRENT')
    # current_network_settings = get_current_settings('NETWORK-CURRENT')

    # ser = serial.serial_for_url(current_device_settings['serial_device'], do_not_open=True)
    # ser.baudrate = current_device_settings['baud_rate']

    try:
        ser.open()
        print('serial port opened')
    except serial.SerialException as e:
        sys.stderr.write('Could not open serial port {}: {}\n'.format(ser.name, e))
        sys.exit(1)

    osc_bridge = SerialToNet()
    serial_thread = serial.threaded.ReaderThread(ser, osc_bridge)
    serial_thread.start()
    print('serial thread started')

    try:
        intentional_exit = False
        while True:
            # console_ip = current_device_settings['console_ip']
            # tcp_port = current_device_settings['tcp_port']
            # host, port = console_ip, tcp_port

            client_socket = socket.socket()

            try:
                client_socket.connect(socket_address)
                print('client socket conected')
            except socket.error as msg:
                sys.stderr.write('WARNING: {}\n'.format(msg))
                time.sleep(5)  # intentional delay on reconnection as client
                continue
            sys.stderr.write('Connected\n')
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            try:
                osc_bridge.socket = client_socket
                while True:
                    try:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        ser.write(data)  # get a bunch of bytes and send them
                    except socket.error as msg:
                        sys.stderr.write('ERROR: {}\n'.format(msg))
                        # probably got disconnected
                        break
            except KeyboardInterrupt:
                intentional_exit = True
                raise
            except socket.error as msg:
                sys.stderr.write('ERROR: {}\n'.format(msg))
            finally:
                osc_bridge.socket = None
                sys.stderr.write('Disconnected\n')
                client_socket.close()
                if not intentional_exit:
                    time.sleep(5)   # intentional delay on reconnection as client
    except KeyboardInterrupt:
        pass

    sys.stderr.write('\n--- exit ---\n')
    serial_thread.stop()

