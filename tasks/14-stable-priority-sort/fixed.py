def order_tasks(tasks):
    """Highest priority first.

    Tasks with equal priority keep the order they had in the input.
    """
    return sorted(tasks, key=lambda task: task["priority"], reverse=True)
