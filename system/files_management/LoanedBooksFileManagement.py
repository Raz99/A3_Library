import pandas as pd
from system.files_management import BooksFileManagement

LOANED_BOOKS_FILE_PATH = r"data\loaned_books.csv"

import pandas as pd
from system.files_management import BooksFileManagement

# Path to save the filtered list of loaned books
LOANED_BOOKS_FILE_PATH = r"data\loaned_books.csv"

def update():
    try:
        # Read the CSV file containing all books
        df = pd.read_csv(BooksFileManagement.BOOKS_FILE_PATH)

        # Filter for loaned books (where 'is_loaned' is "Yes")
        filter_loaned = df['is_loaned'] == "Yes"
        df_filtered = df[filter_loaned]

        # Save the filtered list of loaned books to a new file
        df_filtered.to_csv(LOANED_BOOKS_FILE_PATH, index=False)

    except (FileNotFoundError, PermissionError, KeyError) as e:
        raise RuntimeError(f"File error: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")
