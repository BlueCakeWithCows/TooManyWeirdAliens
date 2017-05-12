from configparser import ConfigParser
from assets import convert
from entity.planets import Planet
from assets import try_texture
from misc import visualise_dict

class System:
    def __init__(self):
        self.system = {}
        self.system_dict = {}
        pass

    def __my_planet_dict(self,planet):
        d= {}
        d[planet.name] =planet
        return d

    def add_planet(self, key, planet):
        self.system_dict[planet.name] = planet
        my_dict = self.__my_planet_dict(planet)

        if planet.target is None:
            self.system[planet.name] = my_dict
            return

        inheritance_list = []
        t = planet.target
        while t is not None:
            inheritance_list.append(t.name)
            t = t.target
        inheritance_list.reverse()
        lowest_parent_dict =  self.system

        for parent in inheritance_list:
            lowest_parent_dict = lowest_parent_dict[parent]

        lowest_parent_dict[planet.name] = my_dict


    def get_planet(self, key):
        if key is None:
            return None
        if self.system_dict.get(key) is None:
            raise ValueError("No such planet " + key + " in system.")
        return self.system_dict.get(key)


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
    return sys

