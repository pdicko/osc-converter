import threading

from config import open_settings
from oscbridge import open_bridge


def launch_config():
    app = open_settings()
    app.run(host='0.0.0.0', debug=False, threaded=True)


if __name__ == "__main__":

    bridge_thread = threading.Thread(target=open_bridge)
    bridge_thread.start()

    launch_config()
