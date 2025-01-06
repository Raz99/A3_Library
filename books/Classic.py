from Book import Book

class Classic(Book):
    def __init__(self, title, author, is_loaned, copies, year):
        super().__init__(self, title, author, is_loaned, copies, year)