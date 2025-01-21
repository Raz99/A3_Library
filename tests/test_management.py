import unittest
from werkzeug.security import check_password_hash
from system import shared
from system.Management import Management
from system.files_management import UsersFileManagement


class TestManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.management = Management()
        cls.username = "test_user"
        cls.password = "password123"
        cls.management.add_user(cls.username, cls.password)

    @classmethod
    def tearDownClass(cls):
        # Remove the user and update the file
        shared.users.pop(-1)
        UsersFileManagement.update()

    def test_login_success(self):
        result = self.management.login(self.username, self.password)
        self.assertTrue(result)

    def test_last_added_user(self):
        last_added_user = shared.users[len(shared.users) - 1]
        self.assertTrue(last_added_user.get_username() == self.username)

    def test_password_hash(self):
        last_added_user = shared.users[len(shared.users) - 1]
        self.assertTrue(check_password_hash(last_added_user.get_password(), self.password))


if __name__ == '__main__':
    unittest.main()