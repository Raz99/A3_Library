import pandas as pd
from system.files_management import BooksFileManagement

# Path to save the list of popular books
POPULAR_BOOKS_FILE_PATH = r"data/popularity_books.csv"

def update():
    """
    Updates the popular books CSV file with the top 10 most popular books.

    Reads the main books CSV file, sorts the books by popularity in descending order,
    and writes the top 10 most popular books to a new CSV file.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(BooksFileManagement.BOOKS_FILE_PATH)

        # Sort the books by popularity in descending order
        df_sort_popularity = df.sort_values(by='popularity', ascending=False)

        # Select the top 10 most popular books
        top_10 = df_sort_popularity.head(10)

        # Save the top 10 most popular books to a new file
        top_10.to_csv(POPULAR_BOOKS_FILE_PATH, index=False)
    except (FileNotFoundError, PermissionError, KeyError) as e:
        raise RuntimeError(f"File or data error: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")