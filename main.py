import threading

from config import open_settings, get_current_settings
from oscbridge import OscBridge


def run(update_flag, restart_flag):

    current_device_settings = get_current_settings('DEVICE-CURRENT')
    bridge = OscBridge(current_device_settings, update_flag, restart_flag)

    bridge_thread = threading.Thread(target=bridge.open_bridge)
    bridge_thread.start()

    update_handler_thread = threading.Thread(target=bridge.close_bridge)
    update_handler_thread.start()


#   ---test---
    print(f'Active threads: {threading.active_count()}\n')
    threads = threading.enumerate()
    for thread in threads:
        print(thread.name)


def restart(update_flag, restart_flag):
    while True:
        restart_flag.wait()
        print('Restarting...')
        run(update_flag, restart_flag)
        restart_flag.clear()


def main():
    update_flag = threading.Event()
    restart_flag = threading.Event()

    restart_handler_thread = threading.Thread(target=restart, args=(update_flag, restart_flag))
    restart_handler_thread.start()

    run(update_flag, restart_flag)

    flask_app = open_settings(update_flag)
    flask_app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
