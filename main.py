from system import shared
from system.Management import Management


def main():
    Management.setup()
    Management.add_user("shir", "1234")
    user = shared.users[0]
    user.add_book("raz1","shir","5", "Fiction","1995")
    user.add_book("raz1","shir","2", "Fiction","1995")
    user.add_book("raz2", "shir", "2", "Fiction", "1995")
    user.remove_book("raz2","shir", "Fiction","1995")
    Management.add_user("raz", "123")
    Management.remove_user("raz")
    user.loan_book("raz1","shir","Fiction","1995")
    user.remove_book("raz1","shir","Fiction","1995") # Try to remove a book that is on loan

if __name__ == '__main__':
    main()