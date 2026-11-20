"""Permission helpers."""


def has_role(roles, wanted):
    for role in roles:
        if role is wanted:
            return True
    return False
