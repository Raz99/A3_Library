from abc import ABC, abstractmethod
from books import Book

# Iterator interface
class Iterator(ABC):
    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def current(self):
        pass

    @abstractmethod
    def reset(self):
        pass

# Concrete Iterator for Books
class BookIterator(Iterator):
    def __init__(self, books):
        self._books = books
        self._index = 0

    def has_next(self):
        return self._index < len(self._books)

    def next(self):
        if self.has_next():
            book = self._books[self._index]
            self._index += 1
            return book
        return None

    def current(self):
        if self._index < len(self._books):
            return self._books[self._index]
        return None

    def reset(self):
        self._index = 0

# Collection interface
class BookCollection(ABC):
    @abstractmethod
    def create_iterator(self):
        pass

# Concrete Collection
class LibraryBookCollection(BookCollection):
    def __init__(self):
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def remove_book(self, book):
        self._books.remove(book)

    def create_iterator(self):
        return BookIterator(self._books)

    def get_books_by_genre(self, genre):
        genre_books = [book for book in self._books if book.genre == genre]
        return BookIterator(genre_books)

    def get_available_books(self):
        available_books = [book for book in self._books if not book.is_loaned]
        return BookIterator(available_books)