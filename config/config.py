from flask import Flask, render_template, request

import oscbridge
from config.forms import DeviceSettings, NetworkSettings
from configparser import ConfigParser


def get_current_settings(section):
    parser = ConfigParser()
    parser.read('config/config.ini')
    parser.read('config.ini')

    return dict(parser.items(section))


def _update_settings():
    form = dict(request.form)

    parser = ConfigParser()
    config = 'config/config.ini'
    parser.read(config)

    if 'submit_device_form' in form:
        section = 'DEVICE-CURRENT'
        form.popitem()
        for key in form.keys():
            parser.set(section, key, form[key])
    elif 'reset_device_form' in form:
        section = 'DEVICE-CURRENT'
        defaults = dict(parser.items('DEVICE-DEFAULTS'))
        for key in defaults.keys():
            parser.set(section, key, defaults[key])
    elif 'submit_network_form' in form:
        section = 'NETWORK-CURRENT'
        form.popitem()
        for key in form.keys():
            parser.set(section, key, form[key])
    elif 'reset_network_form' in form:
        section = 'NETWORK-CURRENT'
        defaults = dict(parser.items('NETWORK-DEFAULTS'))
        for key in defaults.keys():
            parser.set(section, key, defaults[key])

    with open(config, 'w') as file:
        parser.write(file)


def open_settings(event):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5894d4258a390d7d0ef6b3bfa8861fbd'

    @app.route('/', methods=['GET', 'POST'])
    def load_index():
        if request.method == "POST":
            _update_settings()
            event.set()

        current_device_settings = get_current_settings('DEVICE-CURRENT')
        current_network_settings = get_current_settings('NETWORK-CURRENT')
        # will eventually replace with function(s) that get/set network info from
        # the operating system

        device_form = DeviceSettings(current_device_settings)
        network_form = NetworkSettings(current_network_settings)
        return render_template('index.html', device_form=device_form, network_form=network_form)

    return app
