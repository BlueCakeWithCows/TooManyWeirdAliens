import os, sys
from configparser import ConfigParser
from itertools import chain

_config_path= "data/configs/"
_properties = {}


from configparser import ConfigParser
from itertools import chain


def load_configs():
    config_directory = get_path(_config_path)
    config = ConfigParser()
    for file in list_dir(config_directory):
        path = get_path(_config_path + file)
        config.read(path)
    for section in config.sections():
        for o in config.options(section):
            key = section + "." + o
            val = convert(config.get(section, o))
            _properties[key] = val
    print( _properties)


def list_dir(path):
    list = os.listdir(path)
    return list


def get_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)




@property
def value(key):
    return _properties[key]

def convert(val):
    constructors = [int, float, str]
    for c in constructors:
        try:
            return c(val)
        except ValueError:
            pass

load_configs()