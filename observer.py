from configparser import ConfigParser


def get_state():
    parser = ConfigParser()
    parser.read('config/config.ini')
    state = (dict(parser.items('STATE')))
    return state['running'] == 'True'


def set_state(state_bool):
    state = state_bool
    config = 'config/config.ini'
    parser = ConfigParser()
    parser.read(config)
    parser.set('STATE', 'running', state)

    with open(config, 'w') as file:
        parser.write(file)
