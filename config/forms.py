from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired, IPAddress


class DeviceSettings(FlaskForm):
    def __init__(self, config: dict, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.populate_current_values()

    console_ip = StringField('Console IP', validators=[IPAddress(), InputRequired()])
    tcp_port = IntegerField('TCP Port', validators=[InputRequired()])
    serial_device = StringField('Serial device', validators=[InputRequired()])
    baud_rate = IntegerField('Baud rate', validators=[InputRequired()])
    submit = SubmitField('Apply changes')

    def populate_current_values(self):
        if self.config:
            current_config = self.config
            self.console_ip.data = current_config['console-ip']
            self.tcp_port.data = current_config['tcp-port']
            self.serial_device.data = current_config['serial-device']
            self.baud_rate.data = current_config['baud-rate']


class NetworkSettings(FlaskForm):
    def __init__(self, config: dict, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.populate_current_values()

    ip = StringField('IP', validators=[IPAddress(), InputRequired()], default='10.101.60.101')
    subnet_mask = StringField('Subnet mask', validators=[IPAddress(), InputRequired()], default='255.255.0.0')
    gateway = StringField('Gateway', validators=[IPAddress(), InputRequired()], default='10.101.1.1')
    submit = SubmitField('Apply changes')

    def populate_current_values(self):
        if self.config:
            current_config = self.config
            self.ip.data = current_config['ip']
            self.subnet_mask.data = current_config['subnet-mask']
            self.gateway.data = current_config['gateway']
