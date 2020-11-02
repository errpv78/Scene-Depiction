from tkinter import *

root = Tk()

e = Entry(root, width=40, bg="orange", fg="green",
          borderwidth=5)
e.pack()
e.insert(0, 'Name')

def myClick():
    myLabel = Label(root, text=e.get())
    myLabel.pack()

myButton = Button(root, text="Enter URL",
                  # state=DISABLED,
                  padx=100,pady=25, command=myClick,fg="pink", bg="#000000")

myButton.pack()

root.mainloop()

