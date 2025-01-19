from system.files_management import BooksFileManagement, UsersFileManagement, AvailableBooksFileManagment, LoanedBooksFileManagement
from system import shared
from system.User import User
from werkzeug.security import generate_password_hash, check_password_hash

class Management:
    @staticmethod
    def setup():
        """Initialize the library system."""
        BooksFileManagement.setup()
        AvailableBooksFileManagment.update()
        LoanedBooksFileManagement.update()
        UsersFileManagement.setup()

    @staticmethod
    def add_user(username, password):
        """Add a new user to the system."""
        if not username or not password:
            print("Username and password cannot be empty")
            return False

        # Check if user already exists
        for user in shared.users:
            if user.get_username() == username:
                print("This username already exists")
                return False

        # Create new user
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(username, hashed_password)
            shared.users.append(new_user)
            UsersFileManagement.add_user(new_user)
            print("User successfully registered")
            return True

        except Exception as e:
            print(f"Failed to add user: {str(e)}")
            return False

    @staticmethod
    def remove_user(username):
        """Remove a user from the system."""
        for user in shared.users:
            if username == user.get_username():
                shared.users.remove(user)
                UsersFileManagement.update()
                print("User removed successfully")
                return True
        print("Username not found")
        return False

    @staticmethod
    def login(username, password):
        """Authenticate a user."""
        for user in shared.users:
            if user.get_username() == username and check_password_hash(user.get_password(), password):
                return True
        return False

    @staticmethod
    def get_user(username):
        """Get a user by username."""
        for user in shared.users:
            if user.get_username() == username:
                return user
        print("User not found")
