from books.Book import Book

class Satire(Book):
    def __init__(self, title, author, is_loaned, copies, year):
        super().__init__(title, author, is_loaned, copies, year)