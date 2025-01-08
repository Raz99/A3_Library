from system.Management import Management
from system.Librarian import Librarian

def main():
    Management()
    lib = Librarian("shir","1234")
    lib.add_book("raz","shir","No","5", "Fiction",1995)
    lib.remove_book("raz","shir","No","5", "Fiction",1995)

if __name__ == '__main__':
    main()