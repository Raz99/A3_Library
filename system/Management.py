from system.files_management.BooksFileManagement import BooksFileManagement

class Management:
    books = []

    def __init__(self):
        BooksFileManagement.setup()