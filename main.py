import tkinter as tk

from system.Management import Management
from system.gui import GUI

def main():
    window = tk.Tk()
    app = GUI.OpeningForm(window)
    window.mainloop()

if __name__ == '__main__':
    main()