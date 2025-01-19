from system.Management import Management
import tkinter as tk
from system.gui import GUI
from system import shared

def gui_test():
    Management.setup()
    # Management.add_user("shir", "1234")
    window = tk.Tk()
    app = GUI.OpeningForm(window)
    window.mainloop()

def main():
    Management.setup()
    # Management.add_user("shir", "1234")
    # window = tk.Tk()
    # app = GUI.OpeningForm(window)
    # window.mainloop()
    user = shared.users[0]
    # Management.add_user("shir2", "1234")
    # Management.login("shir2", "1234")
    user.add_book("raz1","shir","5", "Fiction","1995")
    # user.add_book("raz1","shir","2", "Fiction","1995")
    # user.add_book("raz2", "shir", "2", "Fiction", "1995")
    # user.remove_book("raz2")
    # Management.add_user("raz", "123")
    # Management.remove_user("raz")
    # user.lend_book("raz1")
    # user.lend_book("raz1")
    # user.remove_book("raz1") # Try to remove a book that is on loan
    # user.return_book("raz1")
    # user.return_book("raz1")
    #user.return_book("raz1")


if __name__ == '__main__':
    # main()
    gui_test()