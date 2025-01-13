import csv
from system import shared

AVAILABLE_BOOKS_FILE_PATH = r"data\available_books.csv"

def update():
    with open(AVAILABLE_BOOKS_FILE_PATH, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=shared.FIELD_NAMES)
        writer.writeheader()

        shared.available_books = [book for book in shared.books if book.is_available()]
        for book in shared.available_books:
            writer.writerow(book.to_dict())