from tkinter import *

root = Tk()
root.title("Video Player App")

enter_url = Label(root, text = "Enter Url: ")
enter_url.grid(row=1, column=1)

url = Entry(root, width=40, bg="white", fg="grey",
          borderwidth=5)
# url.insert(0, 'Enter Url')
url.grid(row=1, column=2)

or_label = Label(root, text = "OR")
or_label.grid(row=3, column=2)

def printVideoUrl():
    video_url = Label(root, text=url.get())
    video_url.grid(row=6,column=2)

submit = Button(root, text="Submit",
                  # state=DISABLED,
                  padx=100,pady=25, command=printVideoUrl,
                  fg="pink", bg="#000000")
submit.grid(row=5, column=2)

root.mainloop()