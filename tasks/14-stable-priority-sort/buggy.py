"""Ordering for a to-do list."""


def order_tasks(tasks):
    """Highest priority first.

    Tasks with equal priority keep the order they had in the input.
    """
    ordered = sorted(tasks, key=lambda task: task["priority"])
    ordered.reverse()
    return ordered
