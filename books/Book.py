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
        if self.is_loaned == "Yes":
            self.popularity = copies
        else:
            self.popularity = 0
        self.waitlist = []

    def set_is_loaned_dict(self, new_dict):
        self.is_loaned_dict = new_dict

    def set_is_loaned(self, value):
        self.is_loaned = value

    def set_popularity(self,pop):
        self.popularity = pop

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
            "is_loaned_dict": self.is_loaned_dict,
            "popularity": self.popularity
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

    def get_popularity(self):
        return self.popularity

    def add_to_waitlist(self, name, number_phone):
        try:
            waiting = {"name" : name , "phone": int(number_phone)}
            self.waitlist.append(waiting)
            return True
        except Exception as e:
            return False

    def remove_from_waitlist(self):
        if self.waitlist:
            self.waitlist.pop(0)

    def get_waitlist(self):
        return self.waitlist

# class WaitlistIterator:
#     def __init__(self, waitlist):
#         self._waitlist = waitlist
#         self._index = 0
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         if self._index < len(self._waitlist):
#             entry = self._waitlist[self._index]
#             self._index += 1
#             #self._waitlist.pop(0)
#             return entry
#         else:
#             raise StopIteration  # סוף הרשימה