import pandas as pd
from system import shared

AVAILABLE_BOOKS_FILE_PATH = r"data\available_books.csv"


def update():
    # Filter available books
    shared.available_books = [book for book in shared.books if book.is_available()]
    # Convert available books to DataFrame
    books_data = [book.to_dict() for book in shared.available_books]
    df = pd.DataFrame(books_data, columns=shared.FIELD_NAMES)
    df.to_csv(AVAILABLE_BOOKS_FILE_PATH, index=False)

def add_available_book(new_book):
    book_data = pd.DataFrame([new_book.to_dict()], columns=shared.FIELD_NAMES)
    book_data.to_csv(AVAILABLE_BOOKS_FILE_PATH, mode='a', header=False, index=False)

