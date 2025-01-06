from abc import ABC, abstractmethod

# Abstract Base Class
class Book(ABC):
    def __init__(self, title, author, is_loaned, copies, year):
        self.title = title
        self.author = author
        self.is_loaned_dict = {i: is_loaned for i in range(copies)}
        self.copies = copies
        self.year = year

    def loan_book(self):
        for i in range(self.copies):
            if self.is_loaned_dict[i] == "No":
                self.is_loaned_dict[i] = "Yes"
                return True
        print("There are no available copies of this book.")
        return False

    def return_book(self):
        for i in range(self.copies):
            if self.is_loaned_dict[i] == "Yes":
                self.is_loaned_dict[i] = "No"
                return True
        print("There are no loaned copies of this book.")
        return False

    def is_available(self):
        for i in range(self.copies):
            if self.is_loaned_dict[i] == "No":
                return True
        return False