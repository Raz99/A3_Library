from abc import ABC
from system.files_management import BooksFileManagement

class Book(ABC):
    """
    Abstract Base Class representing a Book.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        is_loaned (str): Indicates if the book is loaned ("Yes" or "No").
        is_loaned_dict (dict): Dictionary tracking loan status of each copy.
        copies (int): Number of copies of the book.
        year (int): The year the book was published.
        popularity (int): Popularity of the book based on loan status.
        waitlist (list): List of people waiting for the book.
    """

    def __init__(self, title, author, is_loaned, copies, year):
        """
        Initializes a new Book instance.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            is_loaned (str): Indicates if the book is loaned ("Yes" or "No").
            copies (int): Number of copies of the book.
            year (int): The year the book was published.
        """
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
        """
        Sets the loan status dictionary.

        Args:
            new_dict (dict): New loan status dictionary.
        """
        self.is_loaned_dict = new_dict

    def set_is_loaned(self, value):
        """
        Sets the loan status.

        Args:
            value (str): New loan status ("Yes" or "No").
        """
        self.is_loaned = value

    def set_popularity(self, pop):
        """
        Sets the popularity of the book.

        Args:
            pop (int): New popularity value.
        """
        self.popularity = pop

    def is_available(self):
        """
        Checks if any copy of the book is available.

        Returns:
            bool: True if at least one copy is available, False otherwise.
        """
        for value in self.is_loaned_dict.values():
            if value == "No":
                return True
        return False

    def is_loaned_by_dict(self):
        """
        Checks if any copy of the book is loaned.

        Returns:
            bool: True if at least one copy is loaned, False otherwise.
        """
        for key, value in self.is_loaned_dict.items():
            if value == "Yes":
                return True
        return False

    def to_dict(self):
        """
        Converts the book instance to a dictionary.

        Returns:
            dict: Dictionary representation of the book.
        """
        return {
            "title": self.title,
            "author": self.author,
            "is_loaned": self.is_loaned,
            "copies": self.copies,
            "genre": self.get_genre(),
            "year": self.year,
            "is_loaned_dict": self.is_loaned_dict,
            "popularity": self.popularity,
            "wait_list": self.waitlist
        }

    def get_loaned_dict(self):
        """
        Gets the loan status dictionary.

        Returns:
            dict: Loan status dictionary.
        """
        return self.is_loaned_dict

    def get_genre(self):
        """
        Gets the genre of the book based on the class name.

        Returns:
            str: Genre of the book.
        """
        class_name = self.__class__.__name__
        result = class_name

        for i in range(1, len(class_name)):
            if class_name[i].isupper():
                result = class_name[:i] + " " + class_name[i:]

        return result

    def add_copies(self, amount):
        """
        Adds copies of the book.

        Args:
            amount (int): Number of copies to add.
        """
        for _ in range(amount):
            self.is_loaned_dict.update({self.copies: "No"})
            self.copies += 1

    def __eq__(self, other):
        """
        Checks if two book instances are equal based on the title.

        Args:
            other (Book): Another book instance to compare.

        Returns:
            bool: True if the titles are equal, False otherwise.
        """
        if isinstance(other, Book):
            return self.title == other.title
        return False

    def get_title(self):
        """
        Gets the title of the book.

        Returns:
            str: Title of the book.
        """
        return self.title

    def get_author(self):
        """
        Gets the author of the book.

        Returns:
            str: Author of the book.
        """
        return self.author

    def get_year(self):
        """
        Gets the year the book was published.

        Returns:
            int: Year of publication.
        """
        return self.year

    def get_copies(self):
        """
        Gets the number of copies of the book.

        Returns:
            int: Number of copies.
        """
        return self.copies

    def get_is_loaned(self):
        """
        Gets the loan status of the book.

        Returns:
            str: Loan status ("Yes" or "No").
        """
        return self.is_loaned

    def get_popularity(self):
        """
        Gets the popularity of the book.

        Returns:
            int: Popularity value.
        """
        return self.popularity

    def add_to_waitlist(self, name, phone_number):
        """
        Adds a person to the waitlist.

        Args:
            name (str): Name of the person.
            phone_number (str): Phone number of the person.

        Returns:
            bool: True if the person was added to the waitlist, False otherwise.
        """
        if phone_number.isnumeric():
            waiting = {"name": name, "phone": phone_number}
            self.waitlist.append(waiting)
            self.popularity += 1
            BooksFileManagement.update()
            return True
        else:
            return False

    def remove_from_waitlist(self):
        """
        Removes the first person from the waitlist.

        Returns:
            dict: The removed person from the waitlist.
        """
        if self.waitlist:
            return self.waitlist.pop(0)

    def get_waitlist(self):
        """
        Gets the waitlist.

        Returns:
            list: List of people waiting for the book.
        """
        return self.waitlist

    def set_wait_list(self, waitlist):
        """
        Sets the waitlist.

        Args:
            waitlist (list): New waitlist.
        """
        self.waitlist = waitlist