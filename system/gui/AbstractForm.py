import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from books import BookType
from system.Management import Management

TITLE = "Library Management System"
ICON_PATH = "icon.png"

class AbstractForm:
    def __init__(self):
        """Abstract form with common layout logic."""
        self.root = tk.Tk()
        self.create_common_widgets()
        self.create_specific_widgets()
        self.root.mainloop()

    def create_common_widgets(self):
        """Widgets common to all forms."""
        self.root.title(TITLE)
        icon = tk.PhotoImage(file=ICON_PATH)
        self.root.iconphoto(True, icon)

    def create_specific_widgets(self):
        """Abstract method for child classes to implement form-specific widgets."""
        raise NotImplementedError("Subclasses must implement this method")

class LoginForm(AbstractForm):
    def __init__(self):
        super().__init__()
        self.username_label = None
        self.username_entry = None
        self.password_label = None
        self.password_entry = None
        self.submit_button = None

    def create_specific_widgets(self):
        """Implement specific widgets for the login form."""
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.submit_button = tk.Button(self.root, text="Login", command=self.handle_submit)
        self.submit_button.pack()

    def handle_submit(self):
        """Handle login form submission."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if Management.connect_user(username, password):
            print(f"Login submitted: {username}, {password}")
            MenuForm(Management.add_user(username,password))
        else:
            print("Login failed")


class SignupForm(AbstractForm):
    def __init__(self):
        super().__init__()
        self.name_label = None
        self.name_entry = None
        self.password_label = None
        self.password_entry = None
        self.submit_button = None

    def create_specific_widgets(self):
        """Implement specific widgets for the signup form."""
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack()

        self.submit_button = tk.Button(self.root, text="Sign Up", command=self.handle_submit)
        self.submit_button.pack()

    def handle_submit(self):
        """Handle signup form submission."""
        name = self.name_entry.get()
        password = self.password_entry.get()
        print(f"Signup submitted: {name}, {password}")
        MenuForm(Management.add_user(name, password))


class MenuForm(AbstractForm):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def create_specific_widgets(self):
        add_book_button = tk.Button(self.root, text="Add Book", command=lambda: AddBookForm(self.user))
        add_book_button.pack()
        remove_book_button = tk.Button(self.root, text="Remove Book", command=lambda: RemoveBookForm(self.user))
        remove_book_button.pack()

class AddBookForm(MenuForm):
    def __init__(self, user):
        super().__init__(user)
        self.add_book_window = None
        self.title_label = None
        self.title_entry = None
        self.author_label = None
        self.author_entry = None
        self.copies_label = None
        self.copies_entry = None
        self.genre_label = None
        self.genre_combo = None
        self.year_label = None
        self.year_entry = None

    def create_specific_widgets(self):
        # Creates a new window for adding books
        self.add_book_window = tk.Toplevel(self.root)
        self.add_book_window.title("Add Book")
        self.add_book_window.geometry("400x500")

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
        submit_button = tk.Button(self.add_book_window, text="Submit",
                                  command=lambda: self.handle_submit)
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
                self.add_book_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

class RemoveBookForm(MenuForm):
    def __init__(self, user):
        super().__init__(user)
        self.remove_book_window = None
        self.title_label = None
        self.title_entry = None
        self.author_label = None
        self.author_entry = None
        self.copies_label = None
        self.copies_entry = None
        self.genre_label = None
        self.genre_combo = None
        self.year_label = None
        self.year_entry = None

    def create_specific_widgets(self):
        # Creates a new window for removing books
        self.remove_book_window = tk.Toplevel(self.root)
        self.remove_book_window.title("Book's Details")
        self.remove_book_window.geometry("400x500")

        # Creates input fields
        self.title_label = tk.Label(self.remove_book_window, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.remove_book_window)
        self.title_entry.pack()

        self.author_label = tk.Label(self.remove_book_window, text="Author:")
        self.author_label.pack()
        self.author_entry = tk.Entry(self.remove_book_window)
        self.author_entry.pack()

        self.genre_label = tk.Label(self.remove_book_window, text="Genre:")
        self.genre_label.pack()
        self.genre_combo = ttk.Combobox(self.remove_book_window, values=[genre.value for genre in BookType])
        self.genre_combo.pack()

        self.year_label = tk.Label(self.remove_book_window, text="Year:")
        self.year_label.pack()
        self.year_entry = tk.Entry(self.remove_book_window)
        self.year_entry.pack()

        # Adds submit button
        submit_button = tk.Button(self.remove_book_window, text="Submit",
                                  command=lambda: self.handle_submit)
        submit_button.pack(pady=20)

    def handle_submit(self):
            try:
                # Gets values from entries
                title = self.title_entry.get()
                author = self.author_entry.get()
                year = self.year_entry.get()
                genre = self.genre_combo.get()

                # Ensures that all inputs are in use
                if not (title and author and year and genre):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                # Adds a book
                self.user.remove_book(title, author, genre, year)
                messagebox.showinfo("Success", "Book added successfully!")
                self.remove_book_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")