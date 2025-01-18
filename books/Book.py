from abc import ABC, abstractmethod

# Abstract Base Class
class Book(ABC):
    def __init__(self, title, author, is_loaned, copies, year):
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
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

    def set_is_loanded_dict(self, new_dict):
        self.is_loaned_dict.update(new_dict)

    def set_is_loaned(self, value):
        self.is_loaned = value

    def return_book(self):
        for i in range(self.copies):
            if self.is_loaned_dict[i] == "Yes":
                self.is_loaned_dict[i] = "No"
                return True
        print("There are no loaned copies of this book.")
        return False

    def is_available(self):
        for value in self.is_loaned_dict.values():
            if value == "No":
                return True
        return False

    def is_loaned_by_dict(self):
        for key, value in self.is_loaned_dict.items():
            if value == "Yes":
                return True
        return False

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "is_loaned": self.is_loaned,
            "copies": self.copies,
            "genre": self.get_genre(),
            "year": self.year,
            "is_loaned_dict": self.is_loaned_dict
        }

    def get_loaned_dict(self):
        return self.is_loaned_dict

    def get_genre(self):
        class_name = self.__class__.__name__
        result = class_name

        for i in range(1,len(class_name)):
            if class_name[i].isupper():
                result = class_name[:i] + " " + class_name[i:]

        return result


    def add_copies(self, amount):
        for _ in range(amount):
            self.is_loaned_dict.update({self.copies: "No"})
            self.copies += 1

    def __eq__(self, other):
        if isinstance(other,Book):
            return self.title == other.title
            #return self.title == other.title and self.author == other.author and self.get_genre() == other.get_genre() and self.year == other.year
        return False

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_year(self):
        return self.year

    def get_copies(self):
        return self.copies

    def get_is_loaned(self):
        return self.is_loaned