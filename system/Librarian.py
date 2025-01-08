from books import *
from books.BookFactory import BookFactory
from system.Management import Management
from system.files_management import BooksFileManagement

class Librarian:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_book(self, title, author, is_loaned, copies, genre, year):
        new_book = BookFactory.create_book(title, author, is_loaned, int(copies), BookType(genre), int(year))

        found = False
        for book in Management.books:
            if new_book.__eq__(book):
                found = True
                book.add_copy()
                break

        if found:
            BooksFileManagement.update()

        else:
            Management.books.append(new_book)
            BooksFileManagement.add_book(new_book)

    def remove_book(self, title, author):
        pass




