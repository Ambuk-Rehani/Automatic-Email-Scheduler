import configparser

def load_config():
    # Load the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config
