import ast
import pandas as pd
from books import *
from books.BookFactory import BookFactory
from system import shared
from system.files_management import AvailableBooksFileManagment, LoanedBooksFileManagement , PopularityFileManagment

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

    # If the column is_loaned_dict is not in the CSV file, then add it
    if not 'is_loaned_dict' in df.columns:
        # Adds a new column and writes to file
        new_values = [book.get_loaned_dict() for book in shared.books]
        df['is_loaned_dict'] = new_values
        popularity = [book.get_popularity() for book in shared.books]
        df['popularity'] = popularity
        df.to_csv(BOOKS_FILE_PATH, index=False)

    # If the column is_loaned_dict is in the CSV file, then update the books
    else:
        for i, row in df.iterrows():
            dict_data = ast.literal_eval(row["is_loaned_dict"]) # Convert string to dictionary
            shared.books[i].set_is_loaned_dict(dict_data)
            popularity_data= row["popularity"]
            shared.books[i].set_popularity(popularity_data)


def update():
    # Convert list of books to a pandas DataFrame
    books_data = [book.to_dict() for book in shared.books]
    df = pd.DataFrame(books_data, columns=shared.FIELD_NAMES)
    # Write to CSV file
    df.to_csv(BOOKS_FILE_PATH, index=False)
    update_files()


def add_book(new_book):
    # Convert a single book to DataFrame and append to existing CSV
    book_data = pd.DataFrame([new_book.to_dict()], columns=shared.FIELD_NAMES)
    book_data.to_csv(BOOKS_FILE_PATH, mode='a', header=False, index=False)
    update_files()


def update_files():
    AvailableBooksFileManagment.update()
    LoanedBooksFileManagement.update()
    PopularityFileManagment.update()
