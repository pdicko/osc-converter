import threading

from config import open_settings, get_current_settings
from oscbridge import OscBridge


def run(update_flag, restart_flag):
    if update_flag.is_set():
        update_flag.clear()

    current_device_settings = get_current_settings('DEVICE-CURRENT')
    bridge = OscBridge(current_device_settings)

    bridge_thread = threading.Thread(target=bridge.open_bridge, args=(restart_flag,))
    bridge_thread.start()

    update_handler_thread = threading.Thread(target=bridge.close_bridge, args=(update_flag,))
    update_handler_thread.start()

    # restart_handler_thread = threading.Thread(target=restart, args=(update_flag, restart_flag))
    # restart_handler_thread.start()


def restart(update_flag, restart_flag):
    while True:
        restart_flag.wait()
        run(update_flag, restart_flag)
        restart_flag.clear()


def main():
    update_flag = threading.Event()
    restart_flag = threading.Event()

    run(update_flag, restart_flag)

    restart_handler_thread = threading.Thread(target=restart, args=(update_flag, restart_flag))
    restart_handler_thread.start()

    # current_device_settings = get_current_settings('DEVICE-CURRENT')
    # bridge = OscBridge(current_device_settings)
    #
    # bridge_thread = threading.Thread(target=bridge.open_bridge)
    # bridge_thread.start()
    #
    # update_listener_thread = threading.Thread(target=bridge.close_bridge, args=(update_flag,))
    # update_listener_thread.start()

    flask_app = open_settings(update_flag)
    flask_app.run()


if __name__ == "__main__":
    main()

