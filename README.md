# Library Management System

This project involves creating a **Library Management System** using Python. The system is intended for librarians through a graphical user interface built using tkinter. It can be used for management of book inventory, users, borrowing and returning operations, as well as support for advanced searches.

## Project Structure

- `system` - System components
- `gui` - GUI implementation
- `files_management` - File handling and data persistence
- `books` - Classes and implementations related to books
- `data` - Data storage (CSV files)

## Instructions for running the project

### Prerequisites
- Python 3.x
- Required packages:
  - tkinter
  - pandas
  - werkzeug

### Instructions for running the project
1. Run the `main.py` file to start the application.
2. The application will open a window with an option to login/register. You can use the `Enter` button to submit your username and password.
3. After authenticating, use the menu options to navigate through the system.
- The system will automatically save the data while using the operations.
- You can always go back to the main menu using the `Back` button in the edge of the window.
- In the search books window, partial search is supported.
- In the view books window, you need to select one of the options to filter the books. Category option has an extension. The system will display the books that match the criteria.

## Features
### User Management
- User registration and login
- Password hashing for security
- User authentication

### Book Management
- Add new books
- Remove books
- Search books options:
  - Search by title
  - Search by author
  - Search by category
  - Search by year
- View books options:
  - View all books
  - View available books
  - View loaned books
  - View popular books
  - View books by category
- Lend books
- Return books
- Waiting list management for popular books
- Logout

### Logging System
- System actions are logged to `data/logger.txt`
- Different log levels (info, error)
- Logging system implemented using Decorator Pattern

### Data Persistence
- Data is stored in CSV files
- Data is saved to files during each operation
- Data is stored in the `data` directory, files are:
  - `books.csv` - Book data
  - `available_books.csv` - Available book data
  - `loaned_books.csv` - Loaned book data
  - `popular_books.csv` - Popular book data
  - `users.csv` - User data

### Error Handling
- User-friendly error displays using messagebox
- File operation error handling
- Data validation

## Design Patterns Implemented

### 1. Factory Pattern
- BookFactory for creating book instances
- Ensures consistent book object creation
- Handles different book types and validation

### 2. Observer Pattern
- Used for notification system
- Subject (Management) and Observer (User) interfaces
  - Management class implements the Subject interface
  - User class implements the Observer interface
- Implements notification system for waitlist updates (when a book is returned, the system notifies the next user in the waiting list)

### 3. Strategy Pattern
- Different viewing strategies for books
- Implemented through ViewStrategy interface
- Concrete strategies:
  - ViewAllBooks
  - ViewAvailableBooks
  - ViewLoanedBooks
  - ViewPopularBooks
  - ViewByCategory
- Used for viewing books based on different criteria

### 4. Decorator Pattern
- Implemented in logging system
- Base TextLogger component
- Decorators:
  - InfoTextDecorator
  - ErrorTextDecorator
- Used for logging system operations

### 5. Iterator Pattern
- LibraryBookCollection implementation
- Provides a way to iterate books collection
- Used in view books operations

---

## Submitted by:
- Raz Cohen (ID: 208008995)
- Shir Bismuth (ID 314623505)