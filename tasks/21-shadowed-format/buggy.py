"""Text output for a command line tool."""


def render(values, format="short"):
    if format == "short":
        return "%d values" % len(values)
    if format == "long":
        return ", ".join(format(v, ".1f") for v in values)
    raise ValueError("unknown format: %r" % (format,))
