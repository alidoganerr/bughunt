import unittest

from solution import has_role


class HasRoleTest(unittest.TestCase):
    def test_literal_list(self):
        self.assertIs(has_role(["admin", "editor"], "editor"), True)

    def test_missing(self):
        self.assertIs(has_role(["admin", "editor"], "viewer"), False)

    def test_empty(self):
        self.assertIs(has_role([], "admin"), False)

    def test_case_sensitive(self):
        self.assertIs(has_role(["admin"], "Admin"), False)

    def test_roles_parsed_from_text(self):
        roles = "admin,editor,viewer".split(",")
        self.assertIs(has_role(roles, "admin"), True)
        self.assertIs(has_role(roles, "viewer"), True)

    def test_wanted_built_at_runtime(self):
        wanted = "".join(["ed", "itor"])
        self.assertIs(has_role(["admin", "editor"], wanted), True)

    def test_prefix_is_not_a_match(self):
        roles = "administrator".split(",")
        self.assertIs(has_role(roles, "admin"), False)


if __name__ == "__main__":
    unittest.main()
