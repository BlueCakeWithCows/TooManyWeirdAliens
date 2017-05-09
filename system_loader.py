from configparser import ConfigParser
from assets import convert
from entity.planets import Planet
from assets import try_texture


class System:
    def __init__(self):
        self.planets = {}
        pass

    def add_planet(self, key, planet):
        self.planets[key] = planet

    def get_planet(self, key):
        if key is None:
            return None
        if self.planets.get(key) is None:
            raise ValueError("No such planet " + key + " in system.")
        return self.planets.get(key)


def load_system(file):
    config = ConfigParser()
    config.read(file)
    sys = System()
    for section in config.sections():
        name = section
        dict = {}
        for o in config.options(section):
            key = section + "." + o
            val = convert(config.get(section, o))
            dict[key] = val
        dict.setdefault(None)
        texture = try_texture(dict.get("texture"))
        stellar_body = Planet(None, sys.get_planet(dict.get("target")), dict.get("radius"), texture,
                              dict.get("angle", 0), dict.get("orbit_period"), dict.get("orbit_distance"))
        sys.add_planet(name, stellar_body)
    return sys
