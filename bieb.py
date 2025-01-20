import pandas as pd
import json
from tkinter import *
from PIL import ImageTk
import PIL.Image
from addBooks import *
from viewBooks import *
from editBook import *
from scanISBN import *

with open('info.json','r') as f:
    data = json.load(f)

# owner = data['Owner']
library_name = data['Library_name']

library = pd.read_csv('books.csv', sep=';')
library.drop_duplicates(subset='ISBN', keep='first', inplace=True)

background_color = "#2F1B10"

root = Tk()
root.title(library_name)
background_image = PIL.Image.open("lib.jpg")
[imageSizeWidth, imageSizeHeight] = background_image.size
root.minsize(width=400, height=400)
root.maxsize(width=imageSizeWidth, height=imageSizeHeight)
root.geometry("600x400")

# Keep a reference to the PhotoImage object
img = ImageTk.PhotoImage(background_image)
canvas = Canvas(root, width=imageSizeWidth, height=imageSizeHeight)
canvas.create_image(0, 0, anchor=NW, image=img)
canvas.pack(expand=True, fill=BOTH)

headingFrame1 = Frame(root, bg="black", bd=2)
headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
headingLabel = Label(headingFrame1, text=f"Welcome to \n {library_name}", bg=background_color, fg='white', font=("Helvetica 12 bold", 15))
headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

btn1 = Button(root, text="Add Book", bg=background_color, fg='white', command=lambda :addBook(library))
btn1.place(relx=0.28, rely=0.4, relwidth=0.45, relheight=0.1)

btn2 = Button(root, text="Edit/Delete Book", bg=background_color, fg='white', command=lambda:editBook(library))
btn2.place(relx=0.28, rely=0.5, relwidth=0.45, relheight=0.1)

btn3 = Button(root, text="View Book List", bg=background_color, fg='white', command=lambda:View(root,library))
btn3.place(relx=0.28, rely=0.6, relwidth=0.45, relheight=0.1)

btn4 = Button(root, text="Import Books", bg=background_color, fg='white', command= lambda:importBooks(library))
btn4.place(relx=0.28, rely=0.7, relwidth=0.45, relheight=0.1)

btn5 = Button(root, text='Scan ISBN', bg=background_color, fg='white', command=lambda:scan_isbn(library))
btn5.place(relx=0.28, rely=0.8, relwidth=0.45, relheight=0.1)

btn6 = Button(root, text='Quit', bg=background_color, fg='white', command=root.destroy)
btn6.place(relx=0.28, rely=0.9, relwidth=0.45, relheight=0.1)

root.mainloop()

