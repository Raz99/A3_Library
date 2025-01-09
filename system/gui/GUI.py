from tkinter import *

def add_book():
    pass

window = Tk() # InstantiHates an instance of a window
window.title("Library")
icon = PhotoImage(file="icon.png")
window.iconphoto(True, icon)
window.geometry("420x420")

button = Button(window,text="Add Book")
button1 = Button(window,text="Remove Book")
button2 = Button(window,text="Search Book")
button3 = Button(window,text="View Books")

button.pack()
button1.pack()
button2.pack()
button3.pack()

window.mainloop()