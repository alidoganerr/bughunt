import unittest

from solution import upload_path


class UploadPathTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(upload_path("/srv/uploads", "a.txt"), "/srv/uploads/a.txt")

    def test_sub_directory(self):
        self.assertEqual(
            upload_path("/srv/uploads", "2024/report.txt"),
            "/srv/uploads/2024/report.txt",
        )

    def test_trailing_slash_on_root(self):
        self.assertEqual(upload_path("/srv/uploads/", "a.txt"), "/srv/uploads/a.txt")

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            upload_path("/srv/uploads", "")

    def test_parent_component(self):
        with self.assertRaises(ValueError):
            upload_path("/srv/uploads", "../secret")

    def test_parent_component_in_the_middle(self):
        with self.assertRaises(ValueError):
            upload_path("/srv/uploads", "a/../../b")

    def test_dotted_names_are_fine(self):
        self.assertEqual(
            upload_path("/srv/uploads", "..cache/.hidden"),
            "/srv/uploads/..cache/.hidden",
        )

    def test_absolute_name(self):
        with self.assertRaises(ValueError):
            upload_path("/srv/uploads", "/etc/passwd")


    def test_parent_component_between_names(self):
        with self.assertRaises(ValueError):
            upload_path("/srv/uploads", "a/../b")


if __name__ == "__main__":
    unittest.main()
