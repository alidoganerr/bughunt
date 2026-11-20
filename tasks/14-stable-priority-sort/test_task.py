import unittest

from solution import order_tasks


def names(tasks):
    return [t["name"] for t in tasks]


def make(*pairs):
    return [{"name": n, "priority": p} for n, p in pairs]


class OrderTasksTest(unittest.TestCase):
    def test_distinct_priorities(self):
        tasks = make(("a", 1), ("b", 3), ("c", 2))
        self.assertEqual(names(order_tasks(tasks)), ["b", "c", "a"])

    def test_ties_keep_input_order(self):
        tasks = make(("a", 1), ("b", 2), ("c", 2))
        self.assertEqual(names(order_tasks(tasks)), ["b", "c", "a"])

    def test_all_equal(self):
        tasks = make(("a", 5), ("b", 5), ("c", 5))
        self.assertEqual(names(order_tasks(tasks)), ["a", "b", "c"])

    def test_negative_priorities(self):
        tasks = make(("a", -1), ("b", 0), ("c", -5))
        self.assertEqual(names(order_tasks(tasks)), ["b", "a", "c"])

    def test_empty_and_single(self):
        self.assertEqual(order_tasks([]), [])
        self.assertEqual(names(order_tasks(make(("a", 1)))), ["a"])

    def test_input_not_modified(self):
        tasks = make(("a", 1), ("b", 2))
        order_tasks(tasks)
        self.assertEqual(names(tasks), ["a", "b"])


if __name__ == "__main__":
    unittest.main()
