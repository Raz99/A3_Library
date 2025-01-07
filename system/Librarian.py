from csv import DictWriter
from Management import BOOKS_FILE_PATH

class Librarian:
    field_names = ['title', 'author', 'is_loaned', 'copies', 'genre', 'year', # Must columns
                   'copies_dict']

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_book(self, book):
        with open(BOOKS_FILE_PATH, 'a') as file:
            dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            file.append(book)
