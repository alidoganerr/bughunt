"""Name lookup for an address form."""


def find_city(cities, name):
    """First city that matches `name`, ignoring case and outer spaces."""
    wanted = name.strip().casefold()
    for city in cities:
        if city.strip().casefold() == wanted:
            return city
    return None
