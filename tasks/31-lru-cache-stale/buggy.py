"""In-memory settings."""

from functools import lru_cache


class Settings:
    def __init__(self, values=None):
        self._values = dict(values or {})

    @lru_cache(maxsize=None)
    def get(self, key):
        """Current value for key; KeyError if it is not set."""
        return self._values[key]

    def set(self, key, value):
        self._values[key] = value
