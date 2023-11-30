from config.config import get_current_settings, open_settings

""" HTML page for user to input serial and tcp info.

A Flask html page with forms for the tcp settings and serial device settings.
This includes the IP Address and OSC port for the console, the device path for the
USB device, and teh IPv4 network info for the bridge. Config data is stored in 
config.ini. Configparser is used to fill in the form fields with the current settings
on load. When the user submits the form with new values, config.ini is updated

TODO:

Right now, the network settings for the bridge device are just updated in config.ini,
but the system's network settings are not changed. That will probably need to be done using
the NetworkManager package which doesn't work on MacOS. Once the program is loaded
onto the Raspberry Pi Zero, there will need to be new code to update the network
settings and restart the script or os if necessary.
"""
