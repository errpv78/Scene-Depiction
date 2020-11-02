from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text="Button clicked!!")
    myLabel.pack()

welcome = Label(root, text='Welcome to the APP!!')
myButton = Button(root, text="Clickme!",
                  # state=DISABLED,
                  padx=100,pady=25, command=myClick,
                  fg="pink", bg="#000000")



welcome.grid(row=0, column=0)


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

myButton.pack() # pack and grid can't be together


root.mainloop()