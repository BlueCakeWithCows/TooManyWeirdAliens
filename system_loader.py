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
            key = o
            val = convert(config.get(section, o))
            dict[key] = val
        dict.setdefault(None)
        print(name, ":",dict)
        texture = try_texture(dict.get("texture"))
        stellar_body = Planet(name, sys.get_planet(dict.get("target")), dict.get("radius"), texture,
                              dict.get("angle", 0), dict.get("orbit_period",0), dict.get("orbit_distance",0))
        sys.add_planet(name, stellar_body)
    return list(sys.planets.values())

