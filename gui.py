"""tkinter gui playground"""

# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import, wildcard-import
# pylint: disable=trailing-whitespace

# Lutz, Mark. Programming Python: Powerful Object-Oriented Programming (p. 87). O'Reilly Media. Kindle Edition. 

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

def reply():
    """handle button press"""
    showinfo(title='popup', message='Button pressed!')

# window = Tk()
# button = Button(window, text='press', command=reply)
# button.pack()
# window.mainloop()

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
for x in range(1, 10):
    ttk.Label(frm, text="Hello, World").grid(column=x, row=x)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()
