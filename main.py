import threading
import time

from config import SettingsPage
from oscbridge import OscBridge


def main():
    # restart_trigger = threading.Event()
    settings_page = SettingsPage()
    current_device_settings = settings_page.get_current_settings('DEVICE-CURRENT')
    bridge = OscBridge(current_device_settings)

    bridge_thread = threading.Thread(target=bridge.open_bridge)
    bridge_thread.start()
    for thread in threading.enumerate():
        print(thread.name)

    observer_thread = threading.Thread(target=bridge.close_bridge)
    observer_thread.start()

    settings_page.bridge = bridge
    flask_app = settings_page.open_settings(bridge.restart_trigger)
    flask_app.run()


if __name__ == "__main__":
    main()
