from config import open_settings


def run_flask():
    flask_app = open_settings()
    flask_app.run(host='0.0.0.0', debug=False, threaded=True)


if __name__ == '__main__':
    run_flask()
