# int32 arithmetic for the register emulator

INT32_MIN = -2 ** 31
INT32_MAX = 2 ** 31 - 1


def add_int32(a, b):
    """Add two signed 32-bit integers, wrapping around on overflow."""
    if not (INT32_MIN <= a <= INT32_MAX and INT32_MIN <= b <= INT32_MAX):
        raise ValueError("operands must fit in a signed 32-bit integer")
    total = (a + b) & 0xFFFFFFFF
    if total > INT32_MAX:
        total -= 2 ** 32
    return total
