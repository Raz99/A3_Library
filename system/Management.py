from system.files_management import BooksFileManagement, UsersFileManagement,AvailableBooksFileManagment
from system import shared
from system.User import User

class Management:
    def __init__(self):
        BooksFileManagement.setup()
        UsersFileManagement.create_file_users()
        AvailableBooksFileManagment.update()

    def add_user(self, username, password):
        for user in shared.users:
            if user.get_username() == username:
                print("This username exists")
                return user
        user = User(username, password)
        shared.users.append(user)
        UsersFileManagement.add_user(user)
        print("User successfully registered")
        return user

    def remove_user(self, username):
        for user in shared.users:
            if username == user.get_username():
                shared.users.remove(user)
                UsersFileManagement.update()
                print("This user remove ")
                return
        print("The username is not found")

    def connect_user(self, username, password):
        for user in shared.users:
            if user.get_username() == username:
                return user.get_password == password
        return False
