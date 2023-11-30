import threading

from config import open_settings, get_current_settings
from oscbridge import OscBridge


def main():
    close_flag = threading.Event()

    current_device_settings = get_current_settings('DEVICE-CURRENT')
    bridge = OscBridge(current_device_settings)

    bridge_thread = threading.Thread(target=bridge.open_bridge)
    bridge_thread.start()

    listener_thread = threading.Thread(target=bridge.close_bridge, args=(close_flag,))
    listener_thread.start()

    flask_app = open_settings(close_flag)
    flask_app.run()


if __name__ == "__main__":
    main()

