"""Configuration access."""


def get_setting(config, key, default=None):
    """Value stored under key, or default when the key is not set."""
    value = config.get(key)
    if value:
        return value
    return default
