import configparser

config = configparser.ConfigParser()
config.read('app/config.ini')


def get_general_config(key):
    return config['general'][key]
