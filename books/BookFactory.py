from books import *

class BookFactory:
    """
    Factory class for creating book instances of various types.
    """

    @staticmethod
    def create_book(title, author, is_loaned, copies, book_type, year):
        """
        Creates a book instance based on the specified type.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            is_loaned (str): Indicates if the book is loaned ("Yes" or "No").
            copies (int): Number of copies of the book.
            book_type (BookType): The type of the book.
            year (int): The year the book was published.

        Returns:
            Book: An instance of a subclass of Book based on the book_type.
        """
        if book_type == BookType.ADVENTURE:
            return Adventure(title, author, is_loaned, copies, year)
        elif book_type == BookType.CLASSIC:
            return Classic(title, author, is_loaned, copies, year)
        elif book_type == BookType.DYSTOPIAN:
            return Dystopian(title, author, is_loaned, copies, year)
        elif book_type == BookType.EPIC_POETRY:
            return EpicPoetry(title, author, is_loaned, copies, year)
        elif book_type == BookType.FANTASY:
            return Fantasy(title, author, is_loaned, copies, year)
        elif book_type == BookType.FICTION:
            return Fiction(title, author, is_loaned, copies, year)
        elif book_type == BookType.GOTHIC_FICTION:
            return GothicFiction(title, author, is_loaned, copies, year)
        elif book_type == BookType.GOTHIC_ROMANCE:
            return GothicRomance(title, author, is_loaned, copies, year)
        elif book_type == BookType.HISTORICAL_FICTION:
            return HistoricalFiction(title, author, is_loaned, copies, year)
        elif book_type == BookType.MODERNISM:
            return Modernism(title, author, is_loaned, copies, year)
        elif book_type == BookType.PHILOSOPHY:
            return Philosophy(title, author, is_loaned, copies, year)
        elif book_type == BookType.PSYCHOLOGICAL_DRAMA:
            return PsychologicalDrama(title, author, is_loaned, copies, year)
        elif book_type == BookType.REALISM:
            return Realism(title, author, is_loaned, copies, year)
        elif book_type == BookType.ROMANCE:
            return Romance(title, author, is_loaned, copies, year)
        elif book_type == BookType.SATIRE:
            return Satire(title, author, is_loaned, copies, year)
        elif book_type == BookType.SCIENCE_FICTION:
            return ScienceFiction(title, author, is_loaned, copies, year)
        elif book_type == BookType.TRAGEDY:
            return Tragedy(title, author, is_loaned, copies, year)
        else:
            raise ValueError(f"Unknown book type: {book_type}")