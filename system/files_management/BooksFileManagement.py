import pandas as pd
from books import *
from books.BookFactory import BookFactory
from system import shared

BOOKS_FILE_PATH = r"data\books.csv"


def setup():
    # Creates a list of books based on the given file
    df = pd.read_csv(BOOKS_FILE_PATH)

    for _, row in df.iterrows():
        current = BookFactory.create_book(
            row["title"],
            row["author"],
            row["is_loaned"],
            int(row["copies"]),
            BookType(row["genre"]),
            int(row["year"])
        )
        shared.books.append(current)

    # Adds a new column and writes to file
    new_values = [book.get_loaned_dict() for book in shared.books]
    df['is_loaned_dict'] = new_values
    df.to_csv(BOOKS_FILE_PATH, index=False)


def update():
    # Convert list of books to a pandas DataFrame
    books_data = [book.to_dict() for book in shared.books]
    df = pd.DataFrame(books_data, columns=shared.FIELD_NAMES)
    # Write to CSV file
    df.to_csv(BOOKS_FILE_PATH, index=False)


def add_book(new_book):
    # Convert a single book to DataFrame and append to existing CSV
    book_data = pd.DataFrame([new_book.to_dict()], columns=shared.FIELD_NAMES)
    book_data.to_csv(BOOKS_FILE_PATH, mode='a', header=False, index=False)