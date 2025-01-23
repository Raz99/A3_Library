from abc import ABC, abstractmethod
from books import *
from books.BookFactory import BookFactory
from system import shared
from system.files_management import BooksFileManagement
from tkinter import messagebox

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        """Update the observer with a message.

        Args:
            message (str): The message to update the observer with.
        """
        pass

class User(Observer):
    def __init__(self, username, password):
        """Initialize a user with a username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        """
        self.username = username
        self.password = password

    def to_dict(self):
        """Convert the user to a dictionary.

        Returns:
            dict: The user as a dictionary.
        """
        return {
            "username": self.username,
            "password": self.password
        }

    def get_username(self):
        """Get the username of the user.

        Returns:
            str: The username of the user.
        """
        return self.username

    def get_password(self):
        """Get the password of the user.

        Returns:
            str: The password of the user.
        """
        return self.password

    def add_book(self, title, author, copies, genre, year):
        """Add a book to the system.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            copies (int): The number of copies of the book.
            genre (str): The genre of the book.
            year (int): The year of the book.
        """
        new_book = BookFactory.create_book(title, author, "No", int(copies), BookType(genre), int(year))
        for book in shared.books:
            # If the book already exists, then update its number of copies
            if new_book.__eq__(book):
                book.add_copies(int(copies))
                BooksFileManagement.update()
                return

        # If the book does not exist, then add it as a new book
        shared.books.append(new_book)
        BooksFileManagement.add_book(new_book)

    def remove_book(self, title):
        """Remove a book from the system.

        Args:
            title (str): The title of the book.

        Returns:
            bool: True if the book was removed, False otherwise.
        """
        for book in shared.books:
            if book.get_title() == title:
                if book.get_is_loaned() == "Yes":
                    print("You can't remove the book. It's on loan")
                    return False
                else:
                    shared.books.remove(book)
                    BooksFileManagement.update()
                return True
        print("The book is not found")
        return False

    def lend_book(self, title):
        """Lend a book to a user.

        Args:
            title (str): The title of the book.

        Returns:
            int: 0 if the book is not available, 1 if the loan was successful, 2 if the book was not found.
        """
        for book in shared.books:
            if book.title == title:
                if not book.is_available():
                    return 0
                else:
                    book_dict = book.get_loaned_dict()
                    for key, value in book_dict.items():
                        if value == 'No':
                            book_dict[int(key)] = 'Yes'
                            book.set_is_loaned_dict(book_dict)

                            if book.get_is_loaned() != "Yes":
                                book.set_is_loaned("Yes")

                            book.set_popularity(book.get_popularity() + 1)
                            BooksFileManagement.update()
                            print("The loan was successful")
                            return 1
                    break
        return 2

    def return_book(self, title):
        """Return a book to the system.

        Args:
            title (str): The title of the book.

        Returns:
            bool: True if the book was returned successfully, False otherwise.
        """
        for book in shared.books:
            if book.title == title:
                if book.get_is_loaned() == "Yes":
                    book_dict = book.get_loaned_dict()
                    for key, value in book_dict.items():
                        if value == 'Yes':
                            book_dict[key] = 'No'
                            book.set_is_loaned_dict(book_dict)
                            if not book.is_loaned_by_dict():  # If the book is not loaned
                                book.set_is_loaned("No")
                            BooksFileManagement.update()

                            waiting_list = book.get_waitlist()
                            if waiting_list:
                                if self.lend_book(book.get_title()) == 1:
                                    book.set_popularity(book.get_popularity() - 1)  # Decrease popularity to avoid double counting
                                    requester = book.remove_from_waitlist()
                                    self.update(f"The book \"{book.get_title()}\" was returned and lent to the following person in the waiting list:\n{requester}")
                                    BooksFileManagement.update()
                            return True  # The book was returned successfully
                break
        return False  # The book was not found

    def update(self, message):
        """Update the user with a message.

        Args:
            message (str): The message to update the user with.
        """
        messagebox.showinfo("Notification", message)