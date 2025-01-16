import tkinter as tk
from tkinter import messagebox, ttk
from books import BookType
from system.Management import Management

TITLE = "Library Management System"
ICON_PATH = "icon.png"

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
        login_button = tk.Button(self.root, text="Log in", command=lambda: LoginForm(self.root))
        login_button.pack()
        register_button = tk.Button(self.root, text="Register", command=lambda: SignupForm(self.root))
        register_button.pack()


class LoginForm(AbstractForm):
    def create_specific_widgets(self):
        """Implement specific widgets for the login form."""
        self.login_window = tk.Tk()
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
        if Management.login(username, password):
            print(f"Login submitted: {username}, {password}")
            MenuForm(Management.add_user(username, password))
        else:
            print("Login failed")


class SignupForm(AbstractForm):
    def create_specific_widgets(self):
        """Implement specific widgets for the signup form."""
        self.signup_window = tk.Tk()
        self.signup_window.title("Sign up")

        self.name_label = tk.Label(self.signup_window, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.signup_window)
        self.name_entry.pack()

        self.password_label = tk.Label(self.signup_window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.signup_window, show="*")
        self.password_entry.pack()

        self.submit_button = tk.Button(self.signup_window, text="Sign Up", command=self.handle_submit)
        self.submit_button.pack()

    def handle_submit(self):
        """Handle signup form submission."""
        name = self.name_entry.get()
        password = self.password_entry.get()
        print(f"Signup submitted: {name}, {password}")
        MenuForm(Management.add_user(name, password))


class MenuForm(AbstractForm):
    def __init__(self, user):
        super().__init__(self.root)
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
        submit_button = tk.Button(self.remove_book_window, text="Submit", command=self.handle_submit)
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

if __name__ == '__main__':
    window = tk.Tk()
    app = OpeningForm(window)
    window.mainloop()