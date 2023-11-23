import threading
import time

import serial.threaded

from config import open_settings
from oscbridge import OscBridge
from config.config import get_current_settings


def main():
    current_device_settings = get_current_settings('DEVICE-CURRENT')

    bridge = OscBridge(current_device_settings)

    # bridge_thread = threading.Thread(target=bridge.open_bridge)
    # bridge_thread.start()
    bridge.open_bridge()

    # bridge_handler_thread = threading.Thread(target=bridge.close_bridge)
    # bridge_handler_thread.start()

    # flask_app = open_settings()
    # flask_app.run(host='0.0.0.0', debug=False, threaded=True)


if __name__ == "__main__":
    main()
