import threading
import serial.threaded

from config import open_settings
from oscbridge import open_bridge
from config.config import get_current_settings


def main():
    current_device_settings = get_current_settings('DEVICE-CURRENT')

    ser = serial.serial_for_url(current_device_settings['serial_device'], do_not_open=True)
    ser.baudrate = current_device_settings['baud_rate']

    console_ip = current_device_settings['console_ip']
    tcp_port = int(current_device_settings['tcp_port'])
    address = (console_ip, tcp_port)

    bridge_thread = threading.Thread(target=open_bridge, args=(ser, address))
    bridge_thread.start()

    flask_app = open_settings()
    flask_app.run(host='0.0.0.0', debug=False, threaded=True)


if __name__ == "__main__":
    main()
