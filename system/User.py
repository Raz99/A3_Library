from books import *
from books.BookFactory import BookFactory
from system import shared
from system.files_management import BooksFileManagement, AvailableBooksFileManagment

class User:
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

    def get_password(self):
        return self.password

    def add_book(self, title, author, copies, genre, year):
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

    def remove_book(self, title, author, genre, year):
        book_to_remove = BookFactory.create_book(title, author, "No", 1, BookType(genre), int(year))
        for book in shared.books:
            if book_to_remove.__eq__(book):
                if book.is_book_loand():
                    print("You can't remove the book. It's on loan")
                    return
                else:
                    shared.books.remove(book_to_remove)
                    BooksFileManagement.update()
                return
        print("the book is not found")

    def loan_book(self, title, author, genre, year):
        book_to_loan = BookFactory.create_book(title, author, "No", 1, BookType(genre), int(year))
        for book in shared.books:
            if book_to_loan.__eq__(book):
                    loaned_dict = book_to_loan.get_loaned_dict()
                    for key, value in loaned_dict.items():
                        if value == 'No':
                            loaned_dict[key] = 'Yes'
                            book.set_is_loanded_dict(loaned_dict)
                            book.set_is_loaned("Yes")
                            BooksFileManagement.update()
                            print("The loan was successful")
                        return True

        return False


