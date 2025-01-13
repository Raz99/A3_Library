from system.Management import Management
from system.Librarian import Librarian

def main():
    m = Management()
    lib = Librarian("shir","1234")
    lib.add_book("raz","shir","5", "Fiction",1995)
    lib.remove_book("raz","shir", "Fiction",1995)
    m.add_user("shir","1234")
    m.add_user("raz","5555")
    m.remove_user("shir")

if __name__ == '__main__':
    main()