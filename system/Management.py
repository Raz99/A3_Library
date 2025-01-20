from abc import ABC, abstractmethod

from system.files_management import (BooksFileManagement, UsersFileManagement, AvailableBooksFileManagment,
                                     LoanedBooksFileManagement, PopularityFileManagment)
from system import shared
from system.User import User
from werkzeug.security import generate_password_hash, check_password_hash

class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def unregister_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self, message):
        pass

class Management(Subject):
    def __init__(self):
        """Initialize the library system."""
        BooksFileManagement.setup()
        AvailableBooksFileManagment.update()
        LoanedBooksFileManagement.update()
        UsersFileManagement.setup()
        PopularityFileManagment.update()

    def add_user(self, username, password):
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
            self.register_observer(new_user)
            # shared.users.append(new_user)
            UsersFileManagement.add_user(new_user)
            print("User successfully registered")
            return True

        except Exception as e:
            print(f"Failed to add user: {str(e)}")
            return False

    # def remove_user(self, username):
    #     """Remove a user from the system."""
    #     for user in shared.users:
    #         if username == user.get_username():
    #             self.unregister_observer(user)
    #             # shared.users.remove(user)
    #             UsersFileManagement.update()
    #             print("User removed successfully")
    #             return True
    #     print("Username not found")
    #     return False

    def login(self, username, password):
        """Authenticate a user."""
        for user in shared.users:
            if user.get_username() == username and check_password_hash(user.get_password(), password):
                return True
        return False

    def get_user(self, username):
        """Get a user by username."""
        for user in shared.users:
            if user.get_username() == username:
                return user
        print("User not found")
        return False

    def register_observer(self, observer):
        """Add an observer to the list."""
        if observer not in shared.users:
            shared.users.append(observer)

    def unregister_observer(self, observer):
        """Remove an observer from the list."""
        if observer in shared.users:
            shared.users.remove(observer)

    def notify_observers(self, message):
        """Notify all observers with a message."""
        for observer in shared.users:
            observer.update(message)
