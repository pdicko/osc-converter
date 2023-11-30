import sys
import socket

import serial.threaded


class SerialToNet(serial.threaded.Protocol):
    """serial->socket"""

    def __init__(self):
        self.socket = None

    def __call__(self):
        return self

    def data_received(self, data):
        if self.socket is not None:
            self.socket.sendall(data)


class OscBridge:
    def __init__(self, settings):
        self.current_device_settings = settings
        self.ser = serial.serial_for_url(self.current_device_settings['serial_device'], do_not_open=True)
        self.ser.baudrate = self.current_device_settings['baud_rate']
        self.console_ip = self.current_device_settings['console_ip']
        self.tcp_port = int(self.current_device_settings['tcp_port'])
        self.address = (self.console_ip, self.tcp_port)
        self.client_socket = socket.socket()
        self.osc_bridge = SerialToNet()
        self.serial_thread = serial.threaded.ReaderThread(self.ser, self.osc_bridge)
        # self.flag = threading.Event()

    def open_bridge(self):
        try:
            self.ser.open()
            sys.stdout.write('Serial port opened\n')
        except serial.SerialException as e:
            sys.stderr.write('Could not open serial port {}: {}\n'.format(self.ser.name, e))
            sys.exit(1)

        self.serial_thread.start()
        sys.stdout.write('Serial thread started\n')

        while True:
            try:
                self.client_socket.connect(self.address)
                sys.stdout.write('Socket connectied\n')
                self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            except socket.error as msg:
                sys.stderr.write('WARNING: {}\n'.format(msg))
                sys.exit(1)

            try:
                self.osc_bridge.socket = self.client_socket
                while True:
                    try:
                        data = self.client_socket.recv(1024)
                        if not data:
                            break
                        self.ser.write(data)
                    except socket.error as msg:
                        sys.stderr.write('WARNING: {}\n'.format(msg))
                        sys.exit(1)
            except socket.error as msg:
                sys.stderr.write('WARNING: {}\n'.format(msg))
                sys.exit(1)
            finally:
                self.osc_bridge.socket = None
                sys.stderr.write('Disconnected\n')
                self.client_socket.close()
                break

        print('closing bridge')

    def close_bridge(self, flag):
        flag.wait()
        print('triggerrrrred')
        self.client_socket.shutdown(socket.SHUT_RDWR)
        flag.clear()
