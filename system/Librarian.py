from books import *
from books.BookFactory import BookFactory
from system import shared
from system.files_management import BooksFileManagement

class Librarian:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password
        }

    def get_username(self):
        return self.username

    def add_book(self, title, author, copies, genre, year):
        new_book = BookFactory.create_book(title, author, "No", int(copies), BookType(genre), int(year))

        for book in shared.books:
            # If book already exists
            if new_book.__eq__(book):
                book.add_copies(int(copies))
                BooksFileManagement.update()
                return

        # If the book does not exist
        shared.books.append(new_book)
        BooksFileManagement.add_book(new_book)

    def remove_book(self, title, author, genre, year):
        book_to_remove = BookFactory.create_book(title, author, "No", 1, BookType(genre), int(year))
        for book in shared.books:
            if book_to_remove.__eq__(book):
                shared.books.remove(book_to_remove)
                BooksFileManagement.update()
                return
        print("the book is not found")











