import csv

from books import *
from books.BookFactory import BookFactory
from system import shared

BOOKS_FILE_PATH = r"data\books.csv"
FIELD_NAMES = ['title', 'author', 'is_loaned', 'copies', 'genre', 'year',  # Must columns
               'copies_dict']

def setup():
    # Creates a list of books based on the given file
    with open(BOOKS_FILE_PATH, 'r') as file:
        reader = csv.DictReader(file)
        lines = list(reader)

        for line in lines:
            current = BookFactory.create_book(line["title"], line["author"], line["is_loaned"], int(line["copies"]),
                                              BookType(line["genre"]), int(line["year"]))
            shared.books.append(current)

    # Adds a new column and writes to file
    update()


def update():
    with open(BOOKS_FILE_PATH, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        for book in shared.books:
            writer.writerow(book.to_dict())


def add_book(new_book):
    with open(BOOKS_FILE_PATH, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writerow(new_book.to_dict())