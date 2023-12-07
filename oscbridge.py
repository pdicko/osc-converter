import sys
import socket
import serial.threaded

from parsers.shutdown_listener import sys_shutdown_request
from sliplib import Driver
from osc4py3 import oscbuildparse

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
    def __init__(self, settings, update_flag, restart_flag):
        self.current_device_settings = settings
        self.ser = serial.serial_for_url(self.current_device_settings['serial_device'], do_not_open=True)
        self.ser.baudrate = self.current_device_settings['baud_rate']
        self.console_ip = self.current_device_settings['console_ip']
        self.tcp_port = int(self.current_device_settings['tcp_port'])
        self.address = (self.console_ip, self.tcp_port)
        self.client_socket = socket.socket()
        self.osc_bridge = SerialToNet()
        self.serial_thread = serial.threaded.ReaderThread(self.ser, self.osc_bridge)
        self.update_flag = update_flag
        self.restart_flag = restart_flag

    def open_bridge(self):
        try:
            self.ser.open()
            sys.stdout.write('Serial port opened\n')
        except serial.SerialException as e:
            sys.stderr.write('Could not open serial port {}: {}\n'.format(self.ser.name, e))
            return

        try:
            self.serial_thread.start()
            sys.stdout.write('Serial thread started\n')
        except serial.SerialException as e:
            sys.stderr.write(str(e))
            return

        while True:
            try:
                self.client_socket.connect(self.address)
                sys.stdout.write('Socket connected\n')
                self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except socket.error as msg:
                sys.stderr.write('WARNING: {}\n'.format(msg))
                sys.stderr.write('Connection failed\n')
                return

            try:
                self.osc_bridge.socket = self.client_socket
                while True:
                    try:
                        data = self.client_socket.recv(1024)
                        if not data:
                            break
                        # self.ser.write(data)
                        # if sys_shutdown_request(data):
                        #     print('SYSTEM SHUTDOWN REQUESTED')
                        d = Driver()
                        messages = d.receive(data)
                        for msg in messages:
                            osc_msg = oscbuildparse.decode_packet(msg)
                            print(osc_msg)
                    except socket.error as msg:
                        print('Socket disconnected')
                        sys.stderr.write('WARNING: {}\n'.format(msg))
                        return
            except socket.error as msg:
                print('Exiting: Serial thread could not connect to socket')
                sys.stderr.write('WARNING: {}\n'.format(msg))
                return

    def close_bridge(self):
        self.update_flag.wait()
        self._shutdown()
        self.update_flag.clear()

    def _shutdown(self):
        print('Shutting down...')
        if self.osc_bridge.socket:
            self.osc_bridge.socket = None
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
            print('Socket connection closed successfully')
        if self.serial_thread.is_alive():
            self.serial_thread.close()
            self.ser.close()
            print('Serial connection closed successfully')

        self.restart_flag.set()

