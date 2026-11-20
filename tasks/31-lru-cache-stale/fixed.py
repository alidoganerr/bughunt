"""In-memory settings."""


class Settings:
    def __init__(self, values=None):
        self._values = dict(values or {})

    def get(self, key):
        """Current value for key; KeyError if it is not set."""
        return self._values[key]

    def set(self, key, value):
        self._values[key] = value
