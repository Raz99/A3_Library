import unittest
from system.Management import Management


class UserTest(unittest.TestCase):
    def setUp(self):
        self.management = Management()
        self.username = "test_user"
        self.password = "password123"
        self.management.add_user(self.username, self.password)
        self.user = self.management.get_user(self.username)\


    def test_add_book(self):
        title = "New Book"
        author = "Author1"
        copies = 5
        genre = "Fiction"
        year = 2021

        





if __name__ == '__main__':
    unittest.main()
