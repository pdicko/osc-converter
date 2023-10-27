from flask import Flask, render_template
from config.forms import DeviceSettings, NetworkSettings
from configparser import ConfigParser


def get_current_settings(section):
    parser = ConfigParser()
    parser.read('config/config.ini')

    return dict(parser.items(section))


def open_settings():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5894d4258a390d7d0ef6b3bfa8861fbd'

    @app.route('/', methods=['GET', 'POST'])
    def open_index():
        current_device_settings = get_current_settings('DEVICE-CURRENT')
        current_network_settings = get_current_settings('NETWORK-CURRENT')
        # will eventually replace with function(s) that get/set network info from
        # the operating system

        device_form = DeviceSettings(current_device_settings)
        network_form = NetworkSettings(current_network_settings)
        return render_template('index.html', device_form=device_form, network_form=network_form)

    return app
