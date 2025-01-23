from abc import ABC, abstractmethod

# Iterator interface
class Iterator(ABC):
    @abstractmethod
    def has_next(self):
        """Check if there are more elements in the collection.

        Returns:
            bool: True if there are more elements, False otherwise.
        """
        pass

    @abstractmethod
    def next(self):
        """Get the next element in the collection.

        Returns:
            object: The next element.
        """
        pass

    @abstractmethod
    def current(self):
        """Get the current element in the collection.

        Returns:
            object: The current element.
        """
        pass

    @abstractmethod
    def reset(self):
        """Reset the iterator to the first element."""
        pass

# Concrete Iterator for Books
class BookIterator(Iterator):
    def __init__(self, books):
        """Initialize the book iterator with a list of books.

        Args:
            books (list): The list of books.
        """
        self._books = books
        self._index = 0

    def has_next(self):
        """Check if there are more books in the collection.

        Returns:
            bool: True if there are more books, False otherwise.
        """
        return self._index < len(self._books)

    def next(self):
        """Get the next book in the collection.

        Returns:
            object: The next book, or None if there are no more books.
        """
        if self.has_next():
            book = self._books[self._index]
            self._index += 1
            return book
        return None

    def current(self):
        """Get the current book in the collection.

        Returns:
            object: The current book, or None if the index is out of range.
        """
        if self._index < len(self._books):
            return self._books[self._index]
        return None

    def reset(self):
        """Reset the iterator to the first book."""
        self._index = 0

# Collection interface
class BookCollection(ABC):
    @abstractmethod
    def create_iterator(self):
        """Create an iterator for the book collection.

        Returns:
            Iterator: The iterator for the collection.
        """
        pass

# Concrete Collection
class LibraryBookCollection(BookCollection):
    def __init__(self):
        """Initialize the library book collection."""
        self._books = []

    def add_book(self, book):
        """Add a book to the collection.

        Args:
            book (object): The book to add.
        """
        self._books.append(book)

    def remove_book(self, book):
        """Remove a book from the collection.

        Args:
            book (object): The book to remove.
        """
        self._books.remove(book)

    def create_iterator(self):
        """Create an iterator for the book collection.

        Returns:
            BookIterator: The iterator for the collection.
        """
        return BookIterator(self._books)

    def get_books_by_genre(self, genre):
        """Get an iterator for books of a specific genre.

        Args:
            genre (str): The genre to filter books by.

        Returns:
            BookIterator: The iterator for books of the specified genre.
        """
        genre_books = [book for book in self._books if book.genre == genre]
        return BookIterator(genre_books)

    def get_available_books(self):
        """Get an iterator for available books.

        Returns:
            BookIterator: The iterator for available books.
        """
        available_books = [book for book in self._books if not book.is_loaned]
        return BookIterator(available_books)