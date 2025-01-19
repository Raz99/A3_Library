import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
from books import BookType
from system import shared
from system.Management import Management
import pandas as pd
from system.files_management.BooksFileManagement import BOOKS_FILE_PATH
from system.files_management.AvailableBooksFileManagment import AVAILABLE_BOOKS_FILE_PATH
from system.files_management.LoanedBooksFileManagement import LOANED_BOOKS_FILE_PATH
from system.files_management.PopularityFileManagment import POPULAR_BOOKS_FILE_PATH
from system.files_management import Logger

TITLE = "Library Management System"
ICON_PATH = r"system\gui\icon.png"

class AbstractForm:
    def __init__(self, root):
        """Abstract form with common layout logic."""
        self.root = root
        self.icon = tk.PhotoImage(file=ICON_PATH)  # Keep a reference to the icon
        self.create_common_widgets()
        self.create_specific_widgets()

    def create_common_widgets(self):
        """Widgets common to all forms."""
        self.root.title(TITLE)
        self.root.iconphoto(True, self.icon)

    def create_specific_widgets(self):
        """Abstract method for child classes to implement form-specific widgets."""
        raise NotImplementedError("Subclasses must implement this method")

class OpeningForm(AbstractForm):
    def create_specific_widgets(self):
        login_button = tk.Button(self.root, text="Login", command=self.open_login)
        login_button.pack()
        register_button = tk.Button(self.root, text="Register", command=self.open_signup)
        register_button.pack()

    def open_login(self):
        self.root.withdraw() # Hide the main window
        login_form = LoginForm(self.root)

    def open_signup(self):
        self.root.withdraw() # Hide the main window
        signup_form = SignupForm(self.root)

class LoginForm(AbstractForm):
    def create_specific_widgets(self):
        """Implement specific widgets for the login form."""
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Log in")

        self.username_label = tk.Label(self.login_window, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack()

        self.submit_button = tk.Button(self.login_window, text="Login", command=self.handle_submit)
        self.submit_button.pack()

    def handle_submit(self):
        """Handle login form submission."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login_window.destroy()
        self.root.withdraw()  # Hide the main window
        if Management.login(username, password):
            print(f"Login submitted: {username}")
            Logger.log_success("logged in successfully")
            MenuForm(self.root, Management.get_user(username))
        else:
            print("Login failed")
            Logger.log_fail("logged in fail")
            self.root.deiconify()  # Show the opening window again if the login fails


class SignupForm(AbstractForm):
    def create_specific_widgets(self):
        """Implement specific widgets for the signup form."""
        self.signup_window = tk.Toplevel(self.root)
        self.signup_window.title("Sign up")

        self.username_label = tk.Label(self.signup_window, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.signup_window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.signup_window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.signup_window, show="*")
        self.password_entry.pack()

        self.submit_button = tk.Button(self.signup_window, text="Sign Up", command=self.handle_submit)
        self.submit_button.pack()

    def handle_submit(self):
        """Handle signup form submission."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if Management.add_user(username, password):
            Logger.log_success("registered successfully")
            self.signup_window.destroy()
            self.root.withdraw()
            MenuForm(self.root, Management.get_user(username))
        else:
            Logger.log_fail("registered fail")

class MenuForm(AbstractForm):
    def __init__(self, root, user):
        super().__init__(root)
        self.user = user

    def create_specific_widgets(self):
        self.menu_window = tk.Toplevel(self.root)
        add_book_button = tk.Button(self.menu_window, text="Add Book", command=self.open_add_book)
        add_book_button.pack()
        remove_book_button = tk.Button(self.menu_window, text="Remove Book", command=self.open_remove_book)
        remove_book_button.pack()
        search_book_button = tk.Button(self.menu_window, text="Search Book", command=self.open_search_book)
        search_book_button.pack()
        view_book_button = tk.Button(self.menu_window, text="View Books", command=self.open_view_books)
        view_book_button.pack()
        lend_book_button = tk.Button(self.menu_window, text="Lend Book", command=self.open_lend_book)
        lend_book_button.pack()
        return_book_button = tk.Button(self.menu_window, text="Return Book", command=self.open_return_book)
        return_book_button.pack()
        logout_button = tk.Button(self.menu_window, text="Logout", command=self.open_logout)
        logout_button.pack()

    def open_add_book(self):
        self.menu_window.withdraw()  # Hide the menu window
        add_book_form = AddBookForm(self.root, self.menu_window, self.user)

    def open_remove_book(self):
        self.menu_window.withdraw()  # Hide the menu window
        remove_book_form = RemoveBookForm(self.root, self.menu_window, self.user)

    def open_search_book(self):
        self.menu_window.withdraw()  # Hide the menu window
        search_book_form = SearchBookForm(self.root, self.menu_window, self.user)

    def open_view_books(self):
        self.menu_window.withdraw()  # Hide the menu window
        view_book_form = ViewBookForm(self.root, self.menu_window, self.user)

    def open_lend_book(self):
        self.menu_window.withdraw()  # Hide the menu window
        lend_book_form = LendBookForm(self.root, self.menu_window, self.user)

    def open_return_book(self):
        self.menu_window.withdraw()  # Hide the menu window
        return_book_form = ReturnBookForm(self.root, self.menu_window, self.user)

    def open_logout(self):
        Logger.log_success("log out successful")
        self.menu_window.destroy() # Close the menu window
        self.root.deiconify() # Show the opening window again

class AddBookForm(AbstractForm):
    def __init__(self, root, menu, user):
        super().__init__(root)
        self.menu_wind = menu
        self.user = user

    def create_specific_widgets(self):
        # Creates a new window for adding books
        self.add_book_window = tk.Toplevel(self.root)
        self.add_book_window.title("Add Book")
        self.add_book_window.geometry("400x300")

        # Creates input fields
        self.title_label = tk.Label(self.add_book_window, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.add_book_window)
        self.title_entry.pack()

        self.author_label = tk.Label(self.add_book_window, text="Author:")
        self.author_label.pack()
        self.author_entry = tk.Entry(self.add_book_window)
        self.author_entry.pack()

        self.copies_label = tk.Label(self.add_book_window, text="Copies:")
        self.copies_label.pack()
        self.copies_entry = tk.Entry(self.add_book_window)
        self.copies_entry.pack()

        self.genre_label = tk.Label(self.add_book_window, text="Genre:")
        self.genre_label.pack()
        self.genre_combo = ttk.Combobox(self.add_book_window, values=[genre.value for genre in BookType])
        self.genre_combo.pack()

        self.year_label = tk.Label(self.add_book_window, text="Year:")
        self.year_label.pack()
        self.year_entry = tk.Entry(self.add_book_window)
        self.year_entry.pack()

        # Adds submit button
        submit_button = tk.Button(self.add_book_window, text="Submit", command=self.handle_submit)
        submit_button.pack(pady=20)

    def handle_submit(self):
        try:
            # Gets values from entries
            title = self.title_entry.get()
            author = self.author_entry.get()
            copies = self.copies_entry.get()
            genre = self.genre_combo.get()
            year = self.year_entry.get()

            # Ensures that all inputs are used
            if not (title and author and year and genre):
                messagebox.showerror("Error", "All fields are required!")
                return

            # Adds a book
            self.user.add_book(title, author, copies, genre, year)
            messagebox.showinfo("Success", "Book added successfully!")
            Logger.log_success("book added successfully")
            self.add_book_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            Logger.log_fail("book added fail")

        finally:
            self.menu_wind.deiconify()  # Show the menu window again


class RemoveBookForm(AbstractForm):
    def __init__(self, root, menu, user):
        super().__init__(root)
        self.menu_wind = menu
        self.user = user

    def create_specific_widgets(self):
        # Creates a new window for removing books
        self.remove_book_window = tk.Toplevel(self.root)
        self.remove_book_window.title("Book's Details")
        self.remove_book_window.geometry("400x300")

        # Creates input fields
        self.title_label = tk.Label(self.remove_book_window, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.remove_book_window)
        self.title_entry.pack()

        # Adds submit button
        submit_button = tk.Button(self.remove_book_window, text="Submit", command=self.handle_submit)
        submit_button.pack(pady=20)

    def handle_submit(self):
        try:
            # Gets values from entries
            title = self.title_entry.get()

            # Ensures that all inputs are in use
            if not title:
                messagebox.showerror("Error", "All fields are required!")
                return

            # Removes a book
            if self.user.remove_book(title):
                messagebox.showinfo("Success", "Book removed successfully!")
                Logger.log_success("book removed successfully")
                self.remove_book_window.destroy()
            else:
                Logger.log_fail("book removed fail")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            Logger.log_fail("book removed fail")

        finally:
            self.menu_wind.deiconify()  # Show the menu window again


class LendBookForm(AbstractForm):
    def __init__(self, root, menu, user):
        super().__init__(root)
        self.menu_wind = menu
        self.user = user

    def create_specific_widgets(self):
        # Creates a new window for removing books
        self.lend_book_window = tk.Toplevel(self.root)
        self.lend_book_window.title("Book's Details")
        self.lend_book_window.geometry("400x300")

        # Creates input fields
        self.title_label = tk.Label(self.lend_book_window, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.lend_book_window)
        self.title_entry.pack()

        # Adds submit button
        submit_button = tk.Button(self.lend_book_window, text="Submit", command=self.handle_submit)
        submit_button.pack(pady=20)

    def handle_submit(self):
        try:
            # Gets values from entries
            title = self.title_entry.get()

            # Ensures that all inputs are in use
            if not title:
                messagebox.showerror("Error", "All fields are required!")
                return

            # Adds a book
            if self.user.lend_book(title):
                messagebox.showinfo("Success", "Book lent successfully!")
                Logger.log_success("book borrowed successfully")
                self.lend_book_window.destroy()
            else:
                Logger.log_fail("book borrowed fail")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            Logger.log_fail("book borrowed fail")

        finally:
            self.menu_wind.deiconify()  # Show the menu window again
            
class ReturnBookForm(AbstractForm):
    def __init__(self, root, menu, user):
        super().__init__(root)
        self.menu_wind = menu
        self.user = user

    def create_specific_widgets(self):
        # Creates a new window for removing books
        self.return_book_form = tk.Toplevel(self.root)
        self.return_book_form.title("Book's Details")
        self.return_book_form.geometry("400x300")

        # Creates input fields
        self.title_label = tk.Label(self.return_book_form, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.return_book_form)
        self.title_entry.pack()

        # Adds submit button
        submit_button = tk.Button(self.return_book_form, text="Submit", command=self.handle_submit)
        submit_button.pack(pady=20)

    def handle_submit(self):
        try:
            # Gets values from entries
            title = self.title_entry.get()

            # Ensures that all inputs are in use
            if not title:
                messagebox.showerror("Error", "All fields are required!")
                return

            # Adds a book
            if self.user.return_book(title):
                messagebox.showinfo("Success", "Book returned successfully!")
                Logger.log_success("book returned successfully")
                self.return_book_form.destroy()
            else:
                Logger.log_fail("book returned fail")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            Logger.log_fail("book returned fail")

        finally:
            self.menu_wind.decionify()  # Show the menu window again

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books, query):
        pass

class SearchByTitle(SearchStrategy):
    def search(self, books, query):
        result = books[books['title'].str.contains(query, case=False, na=False)]
        if result.empty:
            Logger.log_fail(f'Search book "{query}" by name completed fail')
            messagebox.showerror("Attention", "No books found")
        else:
            Logger.log_success(f'Search book "{query}" by by name completed successful.')
        return result

class SearchByAuthor(SearchStrategy):
    def search(self, books, query):
        result = books[books['author'].str.contains(query, case=False, na=False)]
        if result.empty:
            Logger.log_fail(f'Search book "{query}" by author name fail')
            messagebox.showerror("Attention", "No books found")
        else:
            Logger.log_success(f'Search book "{query}" by author name successful')
        return result

class SearchByCategory(SearchStrategy):
    def search(self, books, query):
        return books[books['genre'].str.contains(query, case=False, na=False)]

class SearchByYear(SearchStrategy):
    def search(self, books, query):
        return books[books['year'].str.contains(query, case=False, na=False)]

class BookSearcher:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def search(self, books, query):
        return self.strategy.search(books, query)

class SearchBookForm(AbstractForm):
    def __init__(self, root, menu, user):
        super().__init__(root)
        self.menu_wind = menu
        self.user = user
        self.books = pd.read_csv(BOOKS_FILE_PATH)

    def create_specific_widgets(self):
        self.search_book_form = tk.Toplevel(self.root)
        self.search_book_form.title("Search Book")

        # Search type selection
        self.search_type = tk.StringVar()
        self.search_type.set("Title") # Default search type
        self.search_options = ["Title", "Author", "Category", "Year"]

        self.option_menu = ttk.OptionMenu(self.search_book_form, self.search_type, self.search_type.get(), *self.search_options)
        self.option_menu.pack()

        # Search query entry
        self.query_entry = tk.Entry(self.search_book_form, width=50)
        self.query_entry.pack()

        # Search button
        self.search_button = tk.Button(self.search_book_form, text="Search", command=self.perform_search)
        self.search_button.pack()

        # Result display
        self.result_display = ttk.Treeview(self.search_book_form, columns=shared.FIELD_NAMES, show='headings')
        for header in shared.FIELD_NAMES:
            self.result_display.heading(header, text=header)
        self.result_display.pack()

        # BookSearcher default instance
        self.book_searcher = BookSearcher(SearchByTitle())

        # Bind the close event to the on_closing function
        self.search_book_form.protocol("WM_DELETE_WINDOW", self.on_closing)

    def perform_search(self):
        search_type = self.search_type.get()
        query = self.query_entry.get()

        if not query:
            messagebox.showerror("Invalid Input", "Search query cannot be empty.")
            return

        try:
            if search_type == "Title":
                self.book_searcher.set_strategy(SearchByTitle())
            elif search_type == "Author":
                self.book_searcher.set_strategy(SearchByAuthor())
            elif search_type == "Category":
                self.book_searcher.set_strategy(SearchByCategory())
            elif search_type == "Year":
                self.book_searcher.set_strategy(SearchByYear())

            results = self.book_searcher.search(self.books, query)
            self.display_results(results)

        except Exception as e:
            messagebox.showerror("Search Error", f"An error occurred during the search: {str(e)}")

    def display_results(self, results):
        # Clear the result display
        for row in self.result_display.get_children():
            self.result_display.delete(row)

        # Insert new results
        for _, book in results.iterrows():
            self.result_display.insert("", "end", values=book.to_list())

    def on_closing(self):
        self.menu_wind.deiconify()
        self.search_book_form.destroy()

class ViewStrategy(ABC):
    @abstractmethod
    def view(self):
        pass

class ViewAllBooks(ViewStrategy):
    def view(self):
        read_books = pd.read_csv(BOOKS_FILE_PATH)
        if read_books.empty:
            Logger.log_fail("Displayed all books fail")
            messagebox.showerror("Attention", "No books to display")
        else:
            Logger.log_success("Displayed all books successful")
        return read_books

class ViewAvailableBooks(ViewStrategy):
    def view(self):
        read_books = pd.read_csv(AVAILABLE_BOOKS_FILE_PATH)
        if read_books.empty:
            Logger.log_fail("Displayed available books fail")
            messagebox.showerror("Attention", "No books available to display")
        else:
            Logger.log_success("Displayed available books successful")
        return read_books

class ViewLoanedBooks(ViewStrategy):
    def view(self):
        read_books = pd.read_csv(LOANED_BOOKS_FILE_PATH)
        if read_books.empty:
            Logger.log_fail("Displayed borrowed books fail")
            messagebox.showerror("Attention", "No books loaned to display")
        else:
            Logger.log_success("Displayed borrowed books successful")
        return read_books

class ViewPopularBooks(ViewStrategy):
    def view(self):
        read_books = pd.read_csv(POPULAR_BOOKS_FILE_PATH)
        if read_books.empty:
            Logger.log_fail("displayed fail")
            messagebox.showerror("Attention", "No books Popular to display")
        else:
            Logger.log_success("displayed successful")
        return read_books

class ViewByCategory(ViewStrategy):
    def __init__(self, category):
        super().__init__()
        self.category = category

    def view(self):
        read_books = pd.read_csv(BOOKS_FILE_PATH)
        if read_books.empty:
            Logger.log_fail("displayed fail")
            messagebox.showerror("Attention", "No books in this category to display")
        else:
            Logger.log_success("displayed successful")
        return read_books[read_books['genre'] == self.category]

class BookViewer:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def view(self):
        return self.strategy.view()

class ViewBookForm(AbstractForm):
    def __init__(self, root, menu, user):
        super().__init__(root)
        self.menu_wind = menu
        self.user = user
        self.books = pd.read_csv(BOOKS_FILE_PATH)

    def create_specific_widgets(self):
        self.view_book_form = tk.Toplevel(self.root)
        self.view_book_form.title("View Books")

        # Search type selection
        self.view_type = tk.StringVar()
        self.view_type.set("All Books")

        self.main_menu = tk.Menu(self.view_book_form)
        self.view_book_form.config(menu=self.main_menu)

        self.option_menu = tk.Menu(self.view_book_form, tearoff=0)
        self.option_menu.add_command(label="All Books", command=lambda: self.set_view_type("All Books"))
        self.option_menu.add_command(label="Available Books", command=lambda: self.set_view_type("Available Books"))
        self.option_menu.add_command(label="Loaned Books", command=lambda: self.set_view_type("Loaned Books"))
        self.option_menu.add_command(label="Popular Books", command=lambda: self.set_view_type("Popular Books"))

        category_menu = tk.Menu(self.view_book_form, tearoff=0)
        for genre in BookType:
            category_menu.add_command(label=genre.value, command=lambda category=genre: self.set_view_type(category.value))

        self.main_menu.add_cascade(label="View Options", menu=self.option_menu)
        self.option_menu.add_cascade(label="By Category", menu=category_menu)

        self.result_display = ttk.Treeview(self.view_book_form, columns=shared.FIELD_NAMES, show='headings')
        for header in shared.FIELD_NAMES:
            self.result_display.heading(header, text=header)
        self.result_display.pack()

        self.book_viewer = BookViewer(ViewAllBooks()) # Default view

        self.perform_view()

        self.view_book_form.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_view_type(self, view_type):
        self.view_type.set(view_type)
        self.perform_view()

    def perform_view(self):
        view_type = self.view_type.get()
        self.book_viewer = BookViewer(ViewAllBooks())  # Default view

        try:
            if view_type == "All Books":
                self.book_viewer.set_strategy(ViewAllBooks())
            elif view_type == "Available Books":
                self.book_viewer.set_strategy(ViewAvailableBooks())
            elif view_type == "Loaned Books":
                self.book_viewer.set_strategy(ViewLoanedBooks())
            elif view_type == "Popular Books":
                self.book_viewer.set_strategy(ViewPopularBooks())
            elif view_type in [genre.value for genre in BookType]:
                self.book_viewer.set_strategy(ViewByCategory(view_type))

            results = self.book_viewer.view()
            self.display_results(results)

        except Exception as e:
            messagebox.showerror("View Error", f"An error occurred during the view: {str(e)}")

    def display_results(self, results):
        # Clear the result display
        for row in self.result_display.get_children():
            self.result_display.delete(row)

        # Insert new results
        for _, book in results.iterrows():
            self.result_display.insert("", "end", values=book.to_list())

    def on_closing(self):
        self.menu_wind.deiconify()
        self.view_book_form.destroy()