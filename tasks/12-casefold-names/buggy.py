"""Name lookup for an address form."""


def find_city(cities, name):
    """First city that matches `name`, ignoring case and outer spaces."""
    wanted = name.strip().lower()
    for city in cities:
        if city.strip().lower() == wanted:
            return city
    return None
