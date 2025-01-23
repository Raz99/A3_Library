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
        """Set up the test class with a management instance and a test user."""
        cls.management = Management()
        cls.username = "test_user"
        cls.password = "password123"
        cls.management.add_user(cls.username, cls.password)

    @classmethod
    def tearDownClass(cls):
        """Tear down the test class by removing the test user."""
        if shared.users and shared.users[-1].get_username() == cls.management.get_user(cls.username):
            shared.users.pop(-1)
            UsersFileManagement.update()

    def test_added_user(self):
        """Test if the user was added successfully."""
        last_added_user = shared.users[len(shared.users) - 1]
        self.assertTrue(last_added_user.get_username() == self.username)

    def test_password_hash(self):
        """Test if the password hash matches the original password."""
        last_added_user = shared.users[len(shared.users) - 1]
        self.assertTrue(check_password_hash(last_added_user.get_password(), self.password))

    def test_login_success(self):
        """Test if the login is successful with correct credentials."""
        result = self.management.login(self.username, self.password)
        self.assertTrue(result)

    def test_get_user(self):
        """Test if the user can be retrieved by username."""
        user = self.management.get_user(self.username)
        self.assertTrue(user.get_username() == self.username)

    def test_login_failure(self):
        """Test if the login fails with incorrect password."""
        result = self.management.login(self.username, "wrong_password")
        self.assertFalse(result)

    def test_login_failure_no_user(self):
        """Test if the login fails with non-existent user."""
        result = self.management.login("non_existent_user", "password")
        self.assertFalse(result)

    def test_add_user_empty_username(self):
        """Test if adding a user fails with empty username."""
        result = self.management.add_user("", "password")
        self.assertFalse(result)

    def test_add_user_empty_password(self):
        """Test if adding a user fails with empty password."""
        result = self.management.add_user("username", "")
        self.assertFalse(result)

    def test_add_user_existing_user(self):
        """Test if adding a user fails with an existing username."""
        result = self.management.add_user(self.username, "password")
        self.assertFalse(result)

class TestLogger(unittest.TestCase):
    def setUp(self):
        """Set up the test with a log file."""
        self.log_file = 'test_logger.txt'

    def tearDown(self):
        """Tear down the test by removing the log file."""
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_simple_logger(self):
        """Test if the simple logger logs the correct message."""
        test_message = "Test message"
        logger = SimpleTextLogger(test_message)
        self.assertEqual(logger.log(), test_message)

    def test_info_decorator(self):
        """Test if the info decorator logs the correct message."""
        test_message = "Test info message"
        simple_logger = SimpleTextLogger(test_message)
        info_logger = InfoTextDecorator(simple_logger)
        self.assertEqual(info_logger.log(), test_message)

    def test_error_decorator(self):
        """Test if the error decorator logs the correct message."""
        test_message = "Test error message"
        simple_logger = SimpleTextLogger(test_message)
        error_logger = ErrorTextDecorator(simple_logger)
        self.assertEqual(error_logger.log(), test_message)

class TestGUI(unittest.TestCase):
    def setUp(self):
        """Set up the test with a Tkinter root window."""
        self.root = tk.Tk()

    def tearDown(self):
        """Tear down the test by destroying the Tkinter root window."""
        self.root.destroy()

    def test_login_form_creation(self):
        """Test if the login form is created with all widgets."""
        login_form = LoginForm(self.root)
        self.assertIsNotNone(login_form.username_entry)
        self.assertIsNotNone(login_form.password_entry)
        self.assertIsNotNone(login_form.submit_button)

    def test_signup_form_creation(self):
        """Test if the signup form is created with all widgets."""
        signup_form = SignupForm(self.root)
        self.assertIsNotNone(signup_form.username_entry)
        self.assertIsNotNone(signup_form.password_entry)
        self.assertIsNotNone(signup_form.submit_button)

class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test class with a management instance, test user, and test book."""
        cls.management = Management()
        cls.username = "test_user"
        cls.password = "password123"
        cls.management.add_user(cls.username, cls.password)
        cls.user = cls.management.get_user(cls.username)

        cls.title = "New Book"
        cls.author = "Author1"
        cls.copies = 5
        cls.genre = "Fiction"
        cls.year = 2021

    @classmethod
    def tearDownClass(cls):
        """Tear down the test class by removing the test user and test book."""
        if shared.users and shared.users[-1].get_username() == cls.management.get_user(cls.username):
            shared.users.pop(-1)
            UsersFileManagement.update()
        if shared.books:
            shared.books.pop(-1)
            BooksFileManagement.update()

    def test_add_book(self):
        """Test if a book is added successfully."""
        self.user.add_book(self.title, self.author, self.copies, self.genre, self.year)
        book = shared.books[-1]
        self.assertEqual(book.get_title(), self.title)
        self.assertEqual(book.get_author(), self.author)
        self.assertEqual(book.get_copies(), self.copies)
        self.assertEqual(book.get_genre(), self.genre)
        self.assertEqual(book.get_year(), self.year)

    def test_lend_book(self):
        """Test if a book is lent successfully."""
        book = shared.books[-1]
        self.assertEqual(book.get_is_loaned(), "No")
        self.user.lend_book(book.get_title())
        self.assertEqual(book.get_is_loaned(), "Yes")

    def test_remove_book(self):
        """Test if a book is removed successfully."""
        self.user.remove_book(self.title)
        book = shared.books[-1]
        self.assertEqual(book.get_title(), self.title)

if __name__ == '__main__':
    unittest.main()