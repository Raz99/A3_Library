import unittest
from werkzeug.security import check_password_hash
from system import shared
from system.Management import Management
from system.files_management import UsersFileManagement, BooksFileManagement


class TestManagement(unittest.TestCase):
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

    def test_added_user(self):
        last_added_user = shared.users[len(shared.users) - 1]
        self.assertTrue(last_added_user.get_username() == self.username)

    def test_password_hash(self):
        last_added_user = shared.users[len(shared.users) - 1]
        self.assertTrue(check_password_hash(last_added_user.get_password(), self.password))

    def test_login_success(self):
        result = self.management.login(self.username, self.password)
        self.assertTrue(result)

    def test_get_user(self):
        user = self.management.get_user(self.username)
        self.assertTrue(user.get_username() == self.username)

    def test_login_failure(self):
        result = self.management.login(self.username, "wrong_password")
        self.assertFalse(result)

    def test_login_failure_no_user(self):
        result = self.management.login("non_existent_user", "password")
        self.assertFalse(result)

    def test_add_user_empty_username(self):
        result = self.management.add_user("", "password")
        self.assertFalse(result)

    def test_add_user_empty_password(self):
        result = self.management.add_user("username", "")
        self.assertFalse(result)

    def test_add_user_existing_user(self):
        result = self.management.add_user(self.username, "password")
        self.assertFalse(result)

class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.management = Management()
        cls.username = "test_user"
        cls.password = "password123"
        cls.management.add_user(cls.username, cls.password)
        cls.user = cls.management.get_user(cls.username)

    @classmethod
    def tearDownClass(cls):
        # Delete test user
        shared.users.pop(-1)
        UsersFileManagement.update()
        # Delete test book
        shared.books.pop(-1)
        BooksFileManagement.update()

    def test_add_book(self):
        title = "New Book4"
        author = "Author1"
        copies = 5
        genre = "Fiction"
        year = 2021

        self.user.add_book(title, author, copies, genre, year)
        book = shared.books[len(shared.books) - 1]
        self.assertEqual(book.get_title(), title)
        self.assertEqual(book.get_author(), author)
        self.assertEqual(book.get_copies(), copies)
        # self.assertEqual(book.get_genre(), BookType(genre))
        self.assertEqual(book.get_year(), year)

if __name__ == '__main__':
    unittest.main()