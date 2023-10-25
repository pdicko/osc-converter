from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, IPAddress


class DeviceSettings(FlaskForm):
    console_ip = StringField('Console IP', validators=[IPAddress(), InputRequired()], default="10.101.90.101")
    tcp_port = IntegerField('TCP Port', validators=[InputRequired()], default=3032)
    serial_device = StringField('Serial device', validators=[InputRequired()], default='/dev/tty.usbserial-1430')
    baud_rate = IntegerField('Baud rate', validators=[InputRequired()], default=15200)


class NetworkSettings(FlaskForm):
    ip = IntegerField('IP', validators=[IPAddress(), InputRequired()], default='10.101.60.101')
    subnet_mask = StringField('Subnet mask', validators=[IPAddress(), InputRequired()], default='255.255.0.0')
    gateway = StringField('Gateway', validators=[IPAddress(), InputRequired()])