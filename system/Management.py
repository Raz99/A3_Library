import csv

from books.BookFactory import BookFactory
from books import *

BOOKS_FILE_PATH = "data/books.csv"

class Management:
    books = []

    def __init__(self):
        self.setup()

    @staticmethod
    def setup():
        with open(BOOKS_FILE_PATH, 'r') as file:
            reader = csv.DictReader(file)
            lines = list(reader)

            for line in lines:
                current = BookFactory.create_book(line["title"], line["author"], line["is_loaned"], int(line["copies"]),
                                                  BookType(line["genre"]), int(line["year"]))
                Management.books.append(current)


        with open(BOOKS_FILE_PATH, "w", newline="") as file:
            field_names = Management.books[0].to_dict().keys()
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for book in Management.books:
                writer.writerow(book.to_dict())