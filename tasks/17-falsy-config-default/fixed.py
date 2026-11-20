"""Configuration access."""


def get_setting(config, key, default=None):
    """Value stored under key, or default when the key is not set."""
    if key in config:
        return config[key]
    return default
