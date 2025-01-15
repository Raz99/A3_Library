from system.Management import Management

def main():
    m = Management()
    user = m.add_user("shir","1234")
    user.add_book("raz1","shir","5", "Fiction","1995")
    user.add_book("raz1","shir","2", "Fiction","1995")
    user.add_book("raz2", "shir", "2", "Fiction", "1995")
    user.remove_book("raz1","shir", "Fiction",1995)
    m.add_user("raz","5555")
    m.remove_user("shir")

if __name__ == '__main__':
    main()