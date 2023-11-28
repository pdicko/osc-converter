import sys
import socket
import threading

import serial.threaded
import time


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
        self.restart_trigger = threading.Event()

    def open_bridge(self):
        if self.restart_trigger.is_set():
            self.restart_trigger.clear()

        try:
            self.ser.open()
            sys.stdout.write('Serial port opened\n')
        except serial.SerialException as e:
            sys.stderr.write('Could not open serial port {}: {}\n'.format(self.ser.name, e))
            sys.exit(1)

        self.serial_thread.start()
        sys.stdout.write('Serial thread started\n')

        try:
            intentional_exit = False
            while True:
                try:
                    self.client_socket.connect(self.address)
                except socket.error as msg:
                    sys.stderr.write('WARNING: {}\n'.format(msg))
                    time.sleep(5)  # intentional delay on reconnection as client
                    continue
                sys.stdout.write('Connected to host\n')
                self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

                try:
                    self.osc_bridge.socket = self.client_socket
                    while True:
                        try:
                            data = self.client_socket.recv(1024)
                            if not data:
                                break
                            self.ser.write(data)  # get a bunch of bytes and send them
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
                    self.osc_bridge.socket = None
                    sys.stderr.write('Disconnected\n')
                    self.client_socket.close()
                    if not intentional_exit:
                        time.sleep(5)  # intentional delay on reconnection as client
        except KeyboardInterrupt:
            pass

        sys.stderr.write('\n--- exit ---\n')
        self.serial_thread.stop()

    def close_bridge(self):
        self.restart_trigger.wait()
        self.serial_thread.stop()
        self.ser.close()
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()
