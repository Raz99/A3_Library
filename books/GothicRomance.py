from Book import Book

class GothicRomance(Book):
    def __init__(self, title, author, is_loaned, copies, year):
        super().__init__(self, title, author, is_loaned, copies, year)