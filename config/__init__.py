from flask import Flask, render_template, request
from forms import DeviceSettings, NetworkSettings
from configparser import ConfigParser


def open_settings():
    current_device_settings = get_current_settings('DEVICE-CURRENT')
    current_network_settings = get_current_settings('NETWORK-CURRENT')
    # will eventually replace with function that pulls network info from
    # the operating system

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def open_index():
        if request.method == "POST":
            pass
            # call function update config.ini then
            # restart the program with new settings
        return render_template('index.html',
                               devices=current_device_settings,
                               network=current_network_settings)

    return app


def get_current_settings(section):
    parser = ConfigParser()
    parser.read('config/config.ini')

    return dict(parser.items(section))
