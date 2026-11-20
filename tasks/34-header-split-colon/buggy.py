"""Header parsing."""


def parse_header(line):
    """Split "Name: value" into ("name", "value")."""
    if ":" not in line:
        raise ValueError("no colon in header line")
    parts = line.split(":")
    return parts[0].strip().lower(), parts[1].strip()
