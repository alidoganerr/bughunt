"""Header parsing."""


def parse_header(line):
    """Split "Name: value" into ("name", "value")."""
    if ":" not in line:
        raise ValueError("no colon in header line")
    name, value = line.split(":", 1)
    return name.strip().lower(), value.strip()
