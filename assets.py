import os, sys
from configparser import ConfigParser
import pygame

_config_path = "data/configs/"
_assets_path = "data/assets/"
_assets_config_path = _assets_path + "settings.cfg"
os.chdir(os.path.dirname(__file__))
value = {}
texture = {}
sound = {}
music = {}
font = {}


def _image(name, options):
    path = get_path(_assets_path + options["url"])
    image = pygame.image.load(path).convert_alpha()
    if "width" in options:
        width = convert(options["width"])
        height = convert(options["height"])
        image = pygame.transform.scale(image, (width, height))
    if "rotation" in options:
        image = pygame.transform.rotate(image, convert(options["rotation"]))
    texture[name] = image


def _sound_effect(name, options):
    path = get_path(_assets_path + options["url"])
    effect = pygame.mixer.Sound(path)
    sound[name] = effect


def _music(name, options):
    path = get_path(_assets_path + options["url"])
    music[name] = path


# map the inputs to the function blocks
_assets_switch = {"music": _music, "image": _image, "sound": _sound_effect}


def load_assets():
    config = ConfigParser()
    config.read(get_path(_assets_config_path))

    for section in config.sections():
        _assets_switch[config.get(section, "type")](section, dict(config.items(section)))
    print(music)
    print(texture)
    print(sound)


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
            value[key] = val
    print(value)


def list_dir(path):
    list = os.listdir(path)
    return list


def get_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def convert(val):
    constructors = [int, float, str]
    for c in constructors:
        try:
            return c(val)
        except ValueError:
            pass


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((300, 300), False)
    load_configs()
    load_assets()
