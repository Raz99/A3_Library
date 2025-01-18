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

    def remove_book(self, title):
        #book_to_remove = BookFactory.create_book(title, author, "No", 1, BookType(genre), int(year))
        for book in shared.books:
            if book.get_title() == title:
                if book.get_is_loaned()== "Yes":
                    print("You can't remove the book. It's on loan")
                    return
                else:
                    shared.books.remove(book)
                    BooksFileManagement.update()
                return
        print("the book is not found")

    def lend_book(self, title):
        #book_to_loan = BookFactory.create_book(title, author, "No", 1, BookType(genre), int(year))
        for book in shared.books:
            if book.title == title:
                    book_dict = book.get_loaned_dict()
                    for key, value in book_dict.items():
                        if value == 'No':
                            book_dict[key] = 'Yes'
                            book.set_is_loanded_dict(book_dict)
                            book.set_is_loaned("Yes")
                            BooksFileManagement.update()
                            print("The loan was successful")
                            return True

        return False


    def return_book(self, title):
        for book in shared.books:
            if book.title == title:
                 if book.get_is_loaned()== "Yes":
                     book_dict = book.get_loaned_dict()
                     for key, value in book_dict.items():
                         if value == 'Yes':
                             book_dict[key] = 'No'
                             book.set_is_loanded_dict(book_dict)
                             pass
                     if book.is_loaned_by_dict() == False:
                         book.set_is_loaned("No")
                     BooksFileManagement.update()
                     return True
                 else:
                     print("the book is not loaned")
                     return False