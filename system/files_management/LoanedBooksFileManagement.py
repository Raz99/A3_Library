import pandas as pd
from system.files_management import BooksFileManagement

LOANED_BOOKS_FILE_PATH = r"data\loaned_books.csv"

def update():
    # Read the CSV file
    df = pd.read_csv(BooksFileManagement.BOOKS_FILE_PATH)
    # Filter for available books (where is_loaned is "Yes")
    filter_loaned = df['is_loaned'] == "Yes"
    df_filtered = df[filter_loaned]
    # Save the filtered dataframe to the available books file
    df_filtered.to_csv(LOANED_BOOKS_FILE_PATH, index=False)