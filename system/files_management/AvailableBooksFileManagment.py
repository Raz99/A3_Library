import pandas as pd
from system.files_management import BooksFileManagement

AVAILABLE_BOOKS_FILE_PATH = r"data\available_books.csv"

def update():
    try:
        # Read the CSV file containing the list of books
        df = pd.read_csv(BooksFileManagement.BOOKS_FILE_PATH)

        # Filter for available books (where 'is_loaned_dict' contains "No")
        filter_available = df['is_loaned_dict'].str.contains("No", na=False)
        df_filtered = df[filter_available]

        # Save the filtered list of available books to a new file
        df_filtered.to_csv(AVAILABLE_BOOKS_FILE_PATH, index=False)
    except (FileNotFoundError, PermissionError) as e:
        raise RuntimeError(f"File error: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")