import ast
import pandas as pd
from books import *
from books.BookFactory import BookFactory
from system import shared
from system.files_management import AvailableBooksFileManagment, LoanedBooksFileManagement, PopularityFileManagment

# Path to the CSV file containing book data
BOOKS_FILE_PATH = r"data/books.csv"

def setup():
    """
    Sets up the book system by reading the books from the CSV file and initializing the shared books list.

    Reads the CSV file, creates book instances using the BookFactory, and populates the shared books list.
    If the 'is_loaned_dict' column is not present in the CSV file, it adds the column and updates the file.
    If the column is present, it updates the book instances with the data from the file.
    """
    try:
        # Creates a list of books based on the given file
        df = pd.read_csv(BOOKS_FILE_PATH)

        # Clear the shared books list
        shared.books.clear()
        for _, row in df.iterrows():
            # Create a book instance and add it to the shared books list
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
                # Convert string to dictionary and update book instance
                dict_data = ast.literal_eval(row["is_loaned_dict"])
                shared.books[i].set_is_loaned_dict(dict_data)
                popularity_data = row["popularity"]
                shared.books[i].set_popularity(popularity_data)
                waitlist_data = ast.literal_eval(row["wait_list"])
                shared.books[i].set_wait_list(waitlist_data)

    except Exception as e:
        raise RuntimeError(f"An error occurred during setup: {e}")

def update():
    """
    Updates the books CSV file with the current state of the shared books list.

    Converts the shared books list to a pandas DataFrame and writes it to the CSV file.
    Also updates auxiliary files by calling the update_files function.
    """
    try:
        # Convert list of books to a pandas DataFrame
        books_data = [book.to_dict() for book in shared.books]
        df = pd.DataFrame(books_data, columns=shared.FIELD_NAMES)
        # Write to CSV file
        df.to_csv(BOOKS_FILE_PATH, mode='w', index=False)
        update_files()
    except Exception as e:
        raise RuntimeError(f"An error occurred during update: {e}")

def add_book(new_book):
    """
    Adds a new book to the books CSV file and updates auxiliary files.

    Converts the new book instance to a pandas DataFrame and appends it to the existing CSV file.
    Also updates auxiliary files by calling the update_files function.

    Args:
        new_book (Book): The new book instance to add.
    """
    try:
        # Convert a single book to DataFrame and append to existing CSV
        book_data = pd.DataFrame([new_book.to_dict()], columns=shared.FIELD_NAMES)
        book_data.to_csv(BOOKS_FILE_PATH, mode='a', header=False, index=False)
        update_files()
    except Exception as e:
        raise RuntimeError(f"An error occurred while adding a book: {e}")

def update_files():
    """
    Updates auxiliary files related to available, loaned, and popular books.

    Calls the update functions of AvailableBooksFileManagment, LoanedBooksFileManagement, and PopularityFileManagment.
    """
    try:
        AvailableBooksFileManagment.update()
        LoanedBooksFileManagement.update()
        PopularityFileManagment.update()
    except Exception as e:
        raise RuntimeError(f"An error occurred while updating auxiliary files: {e}")