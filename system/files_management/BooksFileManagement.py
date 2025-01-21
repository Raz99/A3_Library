import ast
import pandas as pd
from books import *
from books.BookFactory import BookFactory
from system import shared
from system.files_management import AvailableBooksFileManagment, LoanedBooksFileManagement , PopularityFileManagment

BOOKS_FILE_PATH = r"data\books.csv"


def setup():
    try:
        # Creates a list of books based on the given file
        df = pd.read_csv(BOOKS_FILE_PATH)

        shared.books.clear()
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
        if 'is_loaned_dict' not in df.columns:
            # Adds a new column and writes to file
            new_values = [book.get_loaned_dict() for book in shared.books]
            df['is_loaned_dict'] = new_values
            popularity = [book.get_popularity() for book in shared.books]
            df['popularity'] = popularity
            waitlist = [book.get_waitlist() for book in shared.books]
            df['wait_list'] = waitlist
            df.to_csv(BOOKS_FILE_PATH, index=False)

        # If the column is_loaned_dict, popularity and wait_list is in the CSV file,
        # then update the books with the data from the file
        else:
            for i, row in df.iterrows():
                dict_data = ast.literal_eval(row["is_loaned_dict"]) # Convert string to dictionary
                shared.books[i].set_is_loaned_dict(dict_data)
                popularity_data = row["popularity"]
                shared.books[i].set_popularity(popularity_data)
                waitlist_data = ast.literal_eval(row["wait_list"])
                shared.books[i].set_wait_list(waitlist_data)

    except Exception as e:
        raise RuntimeError(f"An error occurred during setup: {e}")


def update():
    try:
        # Convert list of books to a pandas DataFrame
        books_data = [book.to_dict() for book in shared.books]
        df = pd.DataFrame(books_data, columns=shared.FIELD_NAMES)
        # Write to CSV file
        df.to_csv(BOOKS_FILE_PATH, mode='w',index=False)
        update_files()
    except Exception as e:
        raise RuntimeError(f"An error occurred during update: {e}")

def add_book(new_book):
    try:
        # Convert a single book to DataFrame and append to existing CSV
        book_data = pd.DataFrame([new_book.to_dict()], columns=shared.FIELD_NAMES)
        book_data.to_csv(BOOKS_FILE_PATH, mode='a', header=False, index=False)
        update_files()
    except Exception as e:
        raise RuntimeError(f"An error occurred while adding a book: {e}")



def update_files():
    try:
        AvailableBooksFileManagment.update()
        LoanedBooksFileManagement.update()
        PopularityFileManagment.update()
    except Exception as e:
        raise RuntimeError(f"An error occurred while updating auxiliary files: {e}")
