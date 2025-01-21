from abc import ABC, abstractmethod
from system.files_management import BooksFileManagement
from system.files_management import UsersFileManagement
from system.files_management import AvailableBooksFileManagment
from system.files_management import LoanedBooksFileManagement
from system.files_management import PopularityFileManagment
from system import shared
from system.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from system.iterators import LibraryBookCollection


class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def unregister_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self, message):
        pass

class Management(Subject):
    def __init__(self):
        """Initialize the library system."""
        self._book_collection = LibraryBookCollection()  # Add this line
        BooksFileManagement.setup()
        # After loading books from file, add them to the collection
        for book in shared.books:
            self._book_collection.add_book(book)
        AvailableBooksFileManagment.update()
        LoanedBooksFileManagement.update()
        UsersFileManagement.setup()
        PopularityFileManagment.update()

    def get_all_books_iterator(self):
        """Get an iterator for all books in the system."""
        return self._book_collection.create_iterator()

    # def add_book(self, book):
    #     """Add a book to the system."""
    #     self._book_collection.add_book(book)
    #     shared.books.append(book)
    #     BooksFileManagement.update()

    def remove_book(self, book):
        """Remove a book from the system."""
        self._book_collection.remove_book(book)
        if book in shared.books:
            shared.books.remove(book)
        BooksFileManagement.update()

    def add_user(self, username, password):
        """Add a new user to the system."""
        if not username or not password:
            print("Username and password cannot be empty")
            return False

        # Check if user already exists
        for user in shared.users:
            if user.get_username() == username:
                print("This username already exists")
                return False

        # Create new user
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(username, hashed_password)
            self.register_observer(new_user)
            # shared.users.append(new_user)
            UsersFileManagement.add_user(new_user)
            print("User successfully registered")
            return True

        except Exception as e:
            print(f"Failed to add user: {str(e)}")
            return False

    # def remove_user(self, username):
    #     """Remove a user from the system."""
    #     for user in shared.users:
    #         if username == user.get_username():
    #             self.unregister_observer(user)
    #             # shared.users.remove(user)
    #             UsersFileManagement.update()
    #             print("User removed successfully")
    #             return True
    #     print("Username not found")
    #     return False

    def login(self, username, password):
        """Authenticate a user."""
        for user in shared.users:
            if user.get_username() == username and check_password_hash(user.get_password(), password):
                return True
        return False

    def get_user(self, username):
        """Get a user by username."""
        for user in shared.users:
            if user.get_username() == username:
                return user
        print("User not found")
        return False

    def register_observer(self, observer):
        """Add an observer to the list."""
        if observer not in shared.users:
            shared.users.append(observer)

    def unregister_observer(self, observer):
        """Remove an observer from the list."""
        if observer in shared.users:
            shared.users.remove(observer)

    def notify_observers(self, message):
        """Notify all observers with a message."""
        for observer in shared.users:
            observer.update(message)

