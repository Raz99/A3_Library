import csv
from books import BookFactory
from books import *

BOOKS_FILE_PATH = "data/books.csv"

class Management:
    field_names = ['title', 'author', 'is_loaned', 'copies', 'genre', 'year',  # Must-be columns
                   'copies_dict']
    books = []

    def __init__(self):
        self.setup()

    @staticmethod
    def setup():
        with open(BOOKS_FILE_PATH, newline='') as file:
            reader = csv.reader(file)
            lines = list(reader)

            for line in lines[1:]:
                current = BookFactory.create(line[0], line[1], line[2], line[3], BookType(line[4]), line[5])
                Management.books.append(current)

