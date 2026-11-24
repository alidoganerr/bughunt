import json


def load_or_default(text, default=None):
    """Parse JSON text; return default if the text is not valid JSON."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return default
