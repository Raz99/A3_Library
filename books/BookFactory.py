from books import *

class BookFactory:
    @staticmethod
    def create_book(book_type, title, author, is_loaned, copies, year):
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
