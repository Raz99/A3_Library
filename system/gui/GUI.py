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
from system.files_management.Logger import SimpleTextLogger, InfoTextDecorator, ErrorTextDecorator

TITLE = "Library System"
ICON_PATH = r"system\gui\icon.png"

class AbstractForm:
    def __init__(self, root):
        """Abstract form with common layout logic."""
        self.root = root
        self.icon = tk.PhotoImage(file=ICON_PATH)  # Keep a reference to the icon
        self.library_management = Management()
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

        # Bind the close event to the on_closing function
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def open_login(self):
        self.root.withdraw() # Hide the main window
        login_form = LoginForm(self.root)

    def open_signup(self):
        self.root.withdraw() # Hide the main window
        signup_form = SignupForm(self.root)

    def on_closing(self):
        self.root.destroy()

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

        self.username_entry.bind('<Return>', lambda event: self.handle_submit())
        self.password_entry.bind('<Return>', lambda event: self.handle_submit())
        self.login_window.bind('<Return>', lambda event: self.handle_submit())

        # Bind the close event to the on_closing function
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def handle_submit(self):
        """Handle login form submission."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.login_window.destroy()
        self.root.withdraw()  # Hide the main window
        if self.library_management.login(username, password):
            message = SimpleTextLogger("logged in successfully")
            info_logged = InfoTextDecorator(message)
            info_logged.log()
            MenuForm(self.root, self.library_management.get_user(username))
        else:
            message = SimpleTextLogger("logged in fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            messagebox.showerror("Error", "Invalid username or password")
            self.create_specific_widgets() # Re-create the login form

    def on_closing(self):
        self.root.deiconify()
        self.login_window.destroy()


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

        self.username_entry.bind('<Return>', lambda event: self.handle_submit())
        self.password_entry.bind('<Return>', lambda event: self.handle_submit())
        self.signup_window.bind('<Return>', lambda event: self.handle_submit())

        # Bind the close event to the on_closing function
        self.signup_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def handle_submit(self):
        """Handle signup form submission."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.signup_window.destroy()
        self.root.withdraw()  # Hide the main window
        if self.library_management.add_user(username, password):
            messagebox.showinfo("Info", "registered successfully")
            message = SimpleTextLogger("registered successfully")
            info_logged = InfoTextDecorator(message)
            info_logged.log()
            MenuForm(self.root, self.library_management.get_user(username))
        else:
            messagebox.showerror( "Error", "This username already exists")
            message = SimpleTextLogger("registered fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            self.create_specific_widgets() # Re-create the signup form

    def on_closing(self):
        self.root.deiconify()
        self.signup_window.destroy()

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

        # Bind the close event to the on_closing function
        self.menu_window.protocol("WM_DELETE_WINDOW", self.open_logout)

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
        try:
            message = SimpleTextLogger("log out successful")
            info_logged = InfoTextDecorator(message)
            info_logged.log()
            self.menu_window.destroy() # Close the menu window
            self.root.destroy() # Close the main window
        except Exception as e:
            message = SimpleTextLogger("log out fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

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

        # Bind the close event to the on_closing function
        self.add_book_window.protocol("WM_DELETE_WINDOW", self.on_closing)

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
                message = SimpleTextLogger("book added fail")
                error_logged = ErrorTextDecorator(message)
                error_logged.log()
                self.on_closing()
                return

            # Adds a book
            self.user.add_book(title, author, copies, genre, year)
            messagebox.showinfo("Success", "Book added successfully!")
            message = SimpleTextLogger("book added successfully")
            info_logged = InfoTextDecorator(message)
            info_logged.log()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            message = SimpleTextLogger("book added fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()

        finally:
            self.on_closing()

    def on_closing(self):
        self.menu_wind.deiconify()
        self.add_book_window.destroy()


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

        # Bind the close event to the on_closing function
        self.remove_book_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def handle_submit(self):
        try:
            # Gets values from entries
            title = self.title_entry.get()

            # Ensures that all inputs are in use
            if not title:
                messagebox.showerror("Error", "All fields are required!")
                message = SimpleTextLogger("book removed fail")
                error_logged = ErrorTextDecorator(message)
                error_logged.log()
                self.on_closing()
                return

            # Removes a book
            if self.user.remove_book(title):
                messagebox.showinfo("Success", "Book removed successfully!")
                message = SimpleTextLogger("book removed successfully")
                info_logged = ErrorTextDecorator(message)
                info_logged.log()
            else:
                messagebox.showerror("Error", "The book is not found")
                message = SimpleTextLogger("book removed fail")
                error_logged = ErrorTextDecorator(message)
                error_logged.log()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            message = SimpleTextLogger("book removed fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()

        finally:
            self.on_closing()

    def on_closing(self):
        self.menu_wind.deiconify()
        self.remove_book_window.destroy()


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

        # Bind the close event to the on_closing function
        self.lend_book_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def handle_submit(self):
        try:
            # Gets values from entries
            title = self.title_entry.get()

            # Ensures that all inputs are in use
            if not title:
                messagebox.showerror("Error", "All fields are required!")
                message = SimpleTextLogger("book borrowed fail")
                error_logged = ErrorTextDecorator(message)
                error_logged.log()
                self.on_closing()
                return

            # Lends a book
            result = self.user.lend_book(title)

            # 0 - No available copies
            if result == 0:
                self.lend_book_window.destroy()
                wind = WaitListForm(self.root, self.menu_wind, self.user, title)
                messagebox.showinfo("Attention",
                                    "There is no available copy of that book, please add the requester to the waiting list.")
                return

            # 1 - Success
            elif result == 1:
                messagebox.showinfo("Success", "Book lent successfully!")
                message = SimpleTextLogger("book borrowed successfully")
                info_logged = InfoTextDecorator(message)
                info_logged.log()

            # 2 - Book not found
            elif result == 2:
                message = SimpleTextLogger("book borrowed fail")
                error_logged = ErrorTextDecorator(message)
                error_logged.log()
                messagebox.showerror("Error", "Book not found")

            self.on_closing()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            message = SimpleTextLogger("book borrowed fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            self.on_closing()

    def on_closing(self):
        self.menu_wind.deiconify()
        self.lend_book_window.destroy()

class WaitListForm(AbstractForm):
    def __init__(self, root, menu, user, title):
        super().__init__(root)
        self.menu_wind = menu
        self.user = user
        self.title = title

    def create_specific_widgets(self):
        # Creates a new window for add to waitlist
        self.waitlist_form = tk.Toplevel(self.root)
        self.waitlist_form.title("Person's Details")
        self.waitlist_form.geometry("400x300")

        # Creates input fields
        self.name_label = tk.Label(self.waitlist_form, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.waitlist_form)
        self.name_entry.pack()

        self.phone_label = tk.Label(self.waitlist_form, text="Phone:")
        self.phone_label.pack()
        self.phone_entry = tk.Entry(self.waitlist_form)
        self.phone_entry.pack()

        submit_button = tk.Button(self.waitlist_form, text="Submit", command=self.handle_submit)
        submit_button.pack(pady=20)

        # Bind the close event to the on_closing function
        self.waitlist_form.protocol("WM_DELETE_WINDOW", self.on_closing)

    def handle_submit(self):
        try:
            # Gets values from entries
            name = self.name_entry.get()
            phone = self.phone_entry.get()

            # Ensures that all inputs are in use
            if not (name and phone):
                messagebox.showerror("Error", "All fields are required!")
                self.on_closing()
                return

            # Adds person's details to wait list
            iterator = self.library_management.get_all_books_iterator()
            while iterator.has_next():
                book = iterator.next()
                if book.get_title() == self.title:
                    if book.add_to_waitlist(name, phone):
                        messagebox.showinfo("Success", "Person's details has been added to wait list!")
                    else:
                        messagebox.showinfo("Failed", "Adding person's details to wait list has been failed")
                    break

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            self.on_closing()

    def on_closing(self):
        self.waitlist_form.destroy()
        self.menu_wind.deiconify()

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

        # Bind the close event to the on_closing function
        self.return_book_form.protocol("WM_DELETE_WINDOW", self.on_closing)

    def handle_submit(self):
        try:
            # Gets values from entries
            title = self.title_entry.get()

            # Ensures that all inputs are in use
            if not title:
                message = SimpleTextLogger("book returned fail")
                error_logged = ErrorTextDecorator(message)
                error_logged.log()
                messagebox.showerror("Error", "All fields are required!")
                self.on_closing()
                return

            # Returns a book
            if self.user.return_book(title):
                messagebox.showinfo("Success", "Book returned successfully!")
                message = SimpleTextLogger("book returned successfully")
                info_logged = InfoTextDecorator(message)
                info_logged.log()
            else:
                messagebox.showerror("Error", "Failed to return the book.")
                message = SimpleTextLogger("book returned fail")
                error_logged = ErrorTextDecorator(message)
                error_logged.log()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            message = SimpleTextLogger("book returned fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()

        finally:
            self.on_closing()

    def on_closing(self):
        self.menu_wind.deiconify()
        self.return_book_form.destroy()

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books, query):
        pass

class SearchByTitle(SearchStrategy):
    def search(self, books, query):
        result = books[books['title'].str.contains(query, case=False, na=False)]
        if result.empty:
            message = SimpleTextLogger(f"Search book \"{query}\" by name completed fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            messagebox.showerror("Attention", "No books found")
        else:
            message = SimpleTextLogger(f"Search book \"{query}\" by name completed successful.")
            info_logged = InfoTextDecorator(message)
            info_logged.log()
        return result

class SearchByAuthor(SearchStrategy):
    def search(self, books, query):
        result = books[books['author'].str.contains(query, case=False, na=False)]
        if result.empty:
            message = SimpleTextLogger(f"Search book \"{query}\" by author name fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            messagebox.showerror("Attention", "No books found")
        else:
            message = SimpleTextLogger(f"Search book \"{query}\" by author name successful")
            info_logged = InfoTextDecorator(message)
            info_logged.log()
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
            self.result_display.column(header, width=150, minwidth=50, stretch=False) # Width handling
        self.result_display.pack()

        # BookSearcher default instance
        self.book_searcher = BookSearcher(SearchByTitle())

        # Bind the close event to the on_closing function
        self.search_book_form.protocol("WM_DELETE_WINDOW", self.on_closing)

    def perform_search(self):
        search_type = self.search_type.get()
        query = self.query_entry.get()

        # if not query:
        #     messagebox.showerror("Invalid Input", "Search query cannot be empty.")
        #     self.on_closing()
        #     return

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
            self.on_closing()

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
            message = SimpleTextLogger("Displayed all books fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            messagebox.showerror("Attention", "No books to display")

        else:
            message = SimpleTextLogger("Displayed all books successful")
            info_logged = InfoTextDecorator(message)
            info_logged.log()
        return read_books

class ViewAvailableBooks(ViewStrategy):
    def view(self):
        read_books = pd.read_csv(AVAILABLE_BOOKS_FILE_PATH)
        if read_books.empty:
            message = SimpleTextLogger("Displayed available books fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            messagebox.showerror("Attention", "No books available to display")
        else:
            message = SimpleTextLogger("Displayed available books successful")
            info_logged = InfoTextDecorator(message)
            info_logged.log()
        return read_books

class ViewLoanedBooks(ViewStrategy):
    def view(self):
        read_books = pd.read_csv(LOANED_BOOKS_FILE_PATH)
        if read_books.empty:
            message = SimpleTextLogger("Displayed borrowed books fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            messagebox.showerror("Attention", "No books loaned to display")
        else:
            message = SimpleTextLogger("Displayed borrowed books successful")
            info_logged = InfoTextDecorator(message)
            info_logged.log()
        return read_books

class ViewPopularBooks(ViewStrategy):
    def view(self):
        read_books = pd.read_csv(POPULAR_BOOKS_FILE_PATH)
        if read_books.empty:
            message = SimpleTextLogger("displayed fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            messagebox.showerror("Attention", "No books Popular to display")
        else:
            message = SimpleTextLogger("displayed successful")
            info_logged = InfoTextDecorator(message)
            info_logged.log()
        return read_books

class ViewByCategory(ViewStrategy):
    def __init__(self, category):
        super().__init__()
        self.category = category

    def view(self):
        read_books = pd.read_csv(BOOKS_FILE_PATH)
        if read_books.empty:
            message = SimpleTextLogger("displayed fail")
            error_logged = ErrorTextDecorator(message)
            error_logged.log()
            messagebox.showerror("Attention", "No books in this category to display")
        else:
            message = SimpleTextLogger("displayed successful")
            info_logged = InfoTextDecorator(message)
            info_logged.log()
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
        # self.view_type.set("All Books")

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
            self.result_display.column(header, width=150, minwidth=50, stretch=False)  # Width handling
        self.result_display.pack()

        # self.book_viewer = BookViewer(ViewAllBooks()) # Default view

        # self.perform_view()

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
            self.view_book_form.destroy()

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