
_properties = {}


@property
def property(key):
    return _properties[key]

def convert(val):
    constructors = [int, float, str]
    for c in constructors:
        try:
            return c(val)
        except ValueError:
            pass
