from system.files_management import BooksFileManagement, UsersFileManagement
from system import shared
from system.Librarian import Librarian

class Management:
    def __init__(self):
        BooksFileManagement.setup()
        UsersFileManagement.create_file_users()

    def add_user(self, username, password):
        for user in shared.users:
            if user.get_username() == username:
                print("this username exists")
                return
        librarian = Librarian(username,password)
        shared.users.append(librarian)
        UsersFileManagement.add_user(librarian)
        print("User successfully registered")

    def remove_user(self, username):
        for user in shared.users:
            if username==user.get_username():
                shared.users.remove(user)
                UsersFileManagement.update()
                print("this user remove ")
                return
        print("the username is not found")


def main():
    m = Management()
    m.add_user("shir","1234")
    m.add_user("raz","5555")
    m.remove_user("shir")


if __name__ == '__main__':
    main()