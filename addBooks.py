import requests
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as MessageBox
import json
from isbnlib import meta
from utils import *

with open('info.json','r') as f:
    data = json.load(f)

library_name = data['Library_name']
main_owner = data['Owner']


def bookRegister(library):
    book_id = bookInfo1.get()
    owner = bookInfo4.get()
    book_info = get_book_info(book_id)
    if book_info is None:
        MessageBox.showerror("Error", "Book not found")
        return
    # id is max value of ID in library + 1 or if there is a gap in the ID's it will be the first gap or if no ID's it will be 0
    id = determine_next_id(library.ID.to_list())

     
    title, authors, publisher, image = book_info
    print(title, authors, publisher, owner,image)
    library.loc[len(library)] = [id,book_id, title, authors, publisher, owner, image]
    library.drop_duplicates(subset='ISBN', keep='first', inplace=True)
    library.to_csv('books.csv', sep=';', index=False)
    # bookInfo1.delete(0, END)
    # bookInfo4.delete(0, END)
    MessageBox.showinfo("Success", "Book added successfully")
    root.destroy()

def addBook(library):
    global bookInfo1, bookInfo4, canvas, root
    root = Tk()
    root.title(library_name)
    root.minsize(width=400, height=400)
    root.geometry("600x400")
    
    # bookTable = "books" # 
    canvas = Canvas(root)
    
    canvas.config(bg="#ff6e40")
    canvas.pack(expand=True,fill=BOTH)
        
    headingFrame1 = Frame(root,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Add Books", bg='black', fg='white', font=('Courier',15))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(root,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.4)
        
    # Book ID
    lb1 = Label(labelFrame,text="Book ISBN : ", bg='black', fg='white')
    lb1.place(relx=0.05,rely=0.2, relheight=0.08)
        
    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3,rely=0.2, relwidth=0.62, relheight=0.08)
               
    # Book owner
    lb2 = Label(labelFrame,text="Owner : ", bg='black', fg='white')
    lb2.place(relx=0.05,rely=0.65, relheight=0.08)
        
    bookInfo4 = Entry(labelFrame)
    bookInfo4.place(relx=0.3,rely=0.65, relwidth=0.62, relheight=0.08)
        
    # Submit Button
    SubmitBtn = Button(root,text="SUBMIT",bg='#d1ccc0', fg='black', command= lambda:bookRegister(library))
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)
    
    quitBtn = Button(root,text="Quit",bg='#f7f1e3', fg='black', command=root.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    root.mainloop()

# addBook()

def importBooks(library):
    file_path = filedialog.askopenfilename()
    if file_path == '':
        return
    new_books = pd.read_csv(file_path, sep=';')
    for book in new_books.iterrows():
        id = determine_next_id(library.ID.to_list())
        owner = main_owner
        book_id = book[1]['ISBN']
        book_info = get_book_info(book_id)
        if book_info is None:
            print("Book not found")
            continue
        title, authors, publisher, image = book_info
        library.loc[len(library)] = [id,book_id, title, authors, publisher, owner, image]
    library.drop_duplicates(subset='ISBN', keep='first', inplace=True)

    library.to_csv('books.csv', sep=';', index=False)
    MessageBox.showinfo("Success", "Books imported successfully")
