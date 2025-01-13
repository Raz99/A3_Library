import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from books import BookType
from system.Librarian import Librarian
from system.files_management import Logger

TITLE = "Library Management System"
ICON_PATH = "icon.png"

class GUI:
    def __init__(self, librarian):
        self.librarian = librarian
        Logger.create_logger()
        self.window = tk.Tk()
        self.window.title(TITLE)
        icon = tk.PhotoImage(file=ICON_PATH)
        self.window.iconphoto(True, icon)
        self.setup_main_window()
        self.window.mainloop()

    def setup_main_window(self):
        # Main window buttons
        add_book_button = tk.Button(self.window, text="Add Book", command=self.show_add_book_window)
        add_book_button.pack()
        remove_book_button = tk.Button(self.window, text="Remove Book", command=self.show_remove_book_window)
        remove_book_button.pack()

    def show_add_book_window(self):
        # Creates a new window for adding books
        add_book_window = tk.Toplevel(self.window)
        add_book_window.title("Add Book")
        add_book_window.geometry("400x500")

        # Creates input fields
        title_label = tk.Label(add_book_window, text="Title:")
        title_label.pack()
        title_entry = tk.Entry(add_book_window)
        title_entry.pack()

        author_label = tk.Label(add_book_window, text="Author:")
        author_label.pack()
        author_entry = tk.Entry(add_book_window)
        author_entry.pack()

        copies_label = tk.Label(add_book_window, text="Copies:")
        copies_label.pack()
        copies_entry = tk.Entry(add_book_window)
        copies_entry.pack()

        genre_label = tk.Label(add_book_window, text="Genre:")
        genre_label.pack()
        genre_combo = ttk.Combobox(add_book_window, values=[genre.value for genre in BookType])
        genre_combo.pack()

        year_label = tk.Label(add_book_window, text="Year:")
        year_label.pack()
        year_entry = tk.Entry(add_book_window)
        year_entry.pack()

        # Adds submit button
        submit_button = tk.Button(add_book_window, text="Submit",
                                  command=lambda: self.submit_book_from_add(add_book_window, title_entry, author_entry,
                                                                            copies_entry,genre_combo,year_entry))
        submit_button.pack(pady=20)

    def submit_book_from_add(self, add_book_window, title_entry, author_entry, copies_entry, genre_combo, year_entry):
            try:
                # Gets values from entries
                title = title_entry.get()
                author = author_entry.get()
                copies = copies_entry.get()
                genre = genre_combo.get()
                year = year_entry.get()

                # Ensures that all inputs are used
                if not (title and author and year and genre):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                # Adds a book
                self.librarian.add_book(title, author, copies, genre, year)
                Logger.log_success('Book added successfully')
                messagebox.showinfo("Success", "Book added successfully!")
                add_book_window.destroy()

            except Exception as e:
                Logger.log_fail('Failed to add book')
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_remove_book_window(self):
        # Creates a new window for removing books
        remove_book_window = tk.Toplevel(self.window)
        remove_book_window.title("Book's Details")
        remove_book_window.geometry("400x500")

        # Creates input fields
        title_label = tk.Label(remove_book_window, text="Title:")
        title_label.pack()
        title_entry = tk.Entry(remove_book_window)
        title_entry.pack()

        author_label = tk.Label(remove_book_window, text="Author:")
        author_label.pack()
        author_entry = tk.Entry(remove_book_window)
        author_entry.pack()

        genre_label = tk.Label(remove_book_window, text="Genre:")
        genre_label.pack()
        genre_combo = ttk.Combobox(remove_book_window, values=[genre.value for genre in BookType])
        genre_combo.pack()

        year_label = tk.Label(remove_book_window, text="Year:")
        year_label.pack()
        year_entry = tk.Entry(remove_book_window)
        year_entry.pack()

        # Adds submit button
        submit_button = tk.Button(remove_book_window, text="Submit",
                                  command=lambda: self.submit_book_from_remove(remove_book_window, title_entry,
                                                                            author_entry, genre_combo, year_entry))
        submit_button.pack(pady=20)

    def submit_book_from_remove(self, remove_book_window, title_entry, author_entry, genre_combo, year_entry):
            try:
                # Gets values from entries
                title = title_entry.get()
                author = author_entry.get()
                year = year_entry.get()
                genre = genre_combo.get()

                # Ensures that all inputs are in use
                if not (title and author and year and genre):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                # Adds a book
                self.librarian.remove_book(title, author, genre, year)
                Logger.log_success('Book removed successfully')
                messagebox.showinfo("Success", "Book added successfully!")
                remove_book_window.destroy()

            except Exception as e:
                Logger.log_fail('Failed to remove book')
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    # Creates a librarian instance
    librarian = Librarian("shir", "1234")

    # Creates and run the GUI
    gui = GUI(librarian)

if __name__ == "__main__":
    main()