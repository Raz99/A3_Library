import os
import unittest
import tkinter as tk

from werkzeug.security import check_password_hash
from system import shared
from system.Management import Management
from system.files_management import UsersFileManagement, BooksFileManagement
from system.files_management.Logger import SimpleTextLogger, InfoTextDecorator, ErrorTextDecorator
from system.gui.GUI import LoginForm, SignupForm


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
        if shared.users and shared.users[-1].get_username() == cls.management.get_user(cls.username):
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

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log_file = 'test_logger.txt'

    def tearDown(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_simple_logger(self):
        test_message = "Test message"
        logger = SimpleTextLogger(test_message)
        self.assertEqual(logger.log(), test_message)

    def test_info_decorator(self):
        test_message = "Test info message"
        simple_logger = SimpleTextLogger(test_message)
        info_logger = InfoTextDecorator(simple_logger)
        self.assertEqual(info_logger.log(), test_message)

    def test_error_decorator(self):
        test_message = "Test error message"
        simple_logger = SimpleTextLogger(test_message)
        error_logger = ErrorTextDecorator(simple_logger)
        self.assertEqual(error_logger.log(), test_message)

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()

    def tearDown(self):
        self.root.destroy()

    def test_login_form_creation(self):
        login_form = LoginForm(self.root)
        # Verify widgets exist
        self.assertIsNotNone(login_form.username_entry)
        self.assertIsNotNone(login_form.password_entry)
        self.assertIsNotNone(login_form.submit_button)

    def test_signup_form_creation(self):
        signup_form = SignupForm(self.root)
        # Verify widgets exist
        self.assertIsNotNone(signup_form.username_entry)
        self.assertIsNotNone(signup_form.password_entry)
        self.assertIsNotNone(signup_form.submit_button)

class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.management = Management()
        cls.username = "test_user"
        cls.password = "password123"
        cls.management.add_user(cls.username, cls.password)
        cls.user = cls.management.get_user(cls.username)

        # Test book
        cls.title = "New Book"
        cls.author = "Author1"
        cls.copies = 5
        cls.genre = "Fiction"
        cls.year = 2021

    @classmethod
    def tearDownClass(cls):
        # Delete test user
        if shared.users and shared.users[-1].get_username() == cls.management.get_user(cls.username):
            shared.users.pop(-1)
            UsersFileManagement.update()
        # Delete test book
        if shared.books:
            shared.books.pop(-1)
            BooksFileManagement.update()

    def test_add_book(self):
        self.user.add_book(self.title, self.author, self.copies, self.genre, self.year)
        book = shared.books[-1]
        self.assertEqual(book.get_title(), self.title)
        self.assertEqual(book.get_author(), self.author)
        self.assertEqual(book.get_copies(), self.copies)
        self.assertEqual(book.get_genre(), self.genre)
        self.assertEqual(book.get_year(), self.year)

    def test_lend_book(self):
        book = shared.books[-1]
        self.assertEqual(book.get_is_loaned(), "No")
        self.user.lend_book(book.get_title())
        self.assertEqual(book.get_is_loaned(), "Yes")

    def test_remove_book(self):
        self.user.remove_book(self.title)
        book = shared.books[-1]
        self.assertEqual(book.get_title(), self.title)

if __name__ == '__main__':
    unittest.main()