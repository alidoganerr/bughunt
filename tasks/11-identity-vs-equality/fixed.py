"""Permission helpers."""


def has_role(roles, wanted):
    for role in roles:
        if role == wanted:
            return True
    return False
