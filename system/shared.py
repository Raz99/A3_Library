FIELD_NAMES = ['title', 'author', 'is_loaned', 'copies', 'genre', 'year',  # Must columns
               'is_loaned_dict','popularity']
books = []
users = []

def book_by_title(title):
    for book in books:
        if book.get_title()==title:
            return book
    return None