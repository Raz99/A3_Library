import pandas as pd
from system.files_management import BooksFileManagement

POPULAR_BOOKS_FILE_PATH = r"data\popularity_books.csv"

def update():
    # Read the CSV file
    df = pd.read_csv(BooksFileManagement.BOOKS_FILE_PATH)
    df_sort_popularity = df.sort_values(by='popularity', ascending=False)
    top_10 = df_sort_popularity.head(10)
    top_10.to_csv(POPULAR_BOOKS_FILE_PATH, index=False)