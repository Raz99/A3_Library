import unittest

from system import shared
from system.Management import Management
from system.files_management import UsersFileManagement


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.management = Management()
        cls.username = "test_user"
        cls.password = "password123"
        cls.management.add_user(cls.username, cls.password)

    @classmethod
    def tearDownClass(cls):
        # Delete test user
        shared.users.pop(-1)
        UsersFileManagement.update()

    def test_add_book(self):
        user = shared.users[-1]
        book = "Book 1"
        user.add_book(book)
        self.assertTrue(book in shared.books)

if __name__ == '__main__':
    unittest.main()
