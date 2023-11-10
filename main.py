import threading

from config import open_settings
from oscbridge import open_bridge


def main():
    bridge_thread = threading.Thread(target=open_bridge)
    bridge_thread.start()

    flask_app = open_settings()
    flask_app.run(host='0.0.0.0', debug=False, threaded=True)


if __name__ == "__main__":
    main()
