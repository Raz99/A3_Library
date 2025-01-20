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
        pass

class User(Observer):
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
        for book in shared.books:
            if book.get_title() == title:
                if book.get_is_loaned()== "Yes":
                    print("You can't remove the book. It's on loan")
                    return False
                else:
                    shared.books.remove(book)
                    BooksFileManagement.update()
                return True
        print("the book is not found")
        return False

    def lend_book(self, title):
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

                            book.set_popularity(book.get_popularity()+1)
                            BooksFileManagement.update()
                            print("The loan was successful")
                            return 1
                    break
        return 2

    def return_book(self, title):
        for book in shared.books:
            if book.title == title:
                if book.get_is_loaned() == "Yes":
                    book_dict = book.get_loaned_dict()
                    for key, value in book_dict.items():
                        if value == 'Yes':
                            book_dict[key] = 'No'
                            book.set_is_loaned_dict(book_dict)
                            if not book.is_loaned_by_dict(): # If the book is not loaned
                                book.set_is_loaned("No")
                            BooksFileManagement.update()

                            waiting_list = book.get_waitlist()
                            if waiting_list:
                                if self.lend_book(book.get_title()) == 1:
                                    book.set_popularity(book.get_popularity()-1) # Decrease popularity to avoid double counting
                                    requester = book.remove_from_waitlist()
                                    self.update(f"The book \"{book.get_title()}\" was returned and lent to the following person in the waiting list:\n{requester}")
                                    BooksFileManagement.update()
                            return True # The book was returned successfully
                break
        return False # The book was not found

    def update(self, message):
        messagebox.showinfo("Notification", message)