import json
from tkinter import *
from tkinter import messagebox as MessageBox

with open('info.json','r') as f:
    data = json.load(f)

library_name = data['Library_name']


def editBook(library):
    global bookInfo1, bookInfo4, canvas, root
    root = Tk()
    root.title(library_name)
    root.minsize(width=400, height=400)
    root.geometry("600x400")
    canvas = Canvas(root)
    canvas.config(bg="#ff6e40")
    canvas.pack(expand=True, fill=BOTH)
    headingFrame1 = Frame(root, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = Label(headingFrame1, text="Edit/Delete Books", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(root, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)
    # Book ID
    lb1 = Label(labelFrame, text="Book ID : ", bg='black', fg='white')
    lb1.place(relx=0.05, rely=0.2, relheight=0.08)
    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, rely=0.2, relwidth=0.62, relheight=0.08)
    # Book owner
    lb2 = Label(labelFrame, text="Owner : ", bg='black', fg='white')
    lb2.place(relx=0.05, rely=0.65, relheight=0.08)
    bookInfo4 = Entry(labelFrame)
    bookInfo4.place(relx=0.3, rely=0.65, relwidth=0.62, relheight=0.08)
    # Submit Button
    SubmitBtn = Button(root, text="SUBMIT", bg='#d1ccc0', fg='black', command=lambda: bookRegister(library))
    SubmitBtn.place(relx=0.15, rely=0.9, relwidth=0.18, relheight=0.08)
    deleteBtn = Button(root, text="DELETE", bg='#d1ccc0', fg='black', command=lambda: deleteBook(library))
    deleteBtn.place(relx=0.40, rely=0.9, relwidth=0.18, relheight=0.08)
    quitBtn = Button(root, text="Quit", bg='#f7f1e3', fg='black', command=root.destroy)
    quitBtn.place(relx=0.65, rely=0.9, relwidth=0.18, relheight=0.08)
    root.mainloop()

def bookRegister(library):
    book_id = bookInfo1.get()
    owner = bookInfo4.get()
    print(book_id, owner)
    if book_id == "" or owner == "":
        return

    # Convert book_id to the appropriate type (e.g., integer)
    try:
        book_id = int(book_id)
    except ValueError:
        print("Invalid book ID")
        return

    if library[library['ID'] == book_id].empty:
        print("Book not found")
        return

    print(library.loc[library['ID'] == book_id])
    library.loc[library['ID'] == book_id, 'Owner'] = owner
    print(library.loc[library['ID'] == book_id])
    library.to_csv('books.csv', sep=';', index=False)
    MessageBox.showinfo("Success", "Book updated successfully")
    # print("Book updated successfully")
    # root.destroy()
    
def deleteBook(library):
    book_id = bookInfo1.get()
    if book_id == "":
        return

    # Convert book_id to the appropriate type (e.g., integer)
    try:
        book_id = int(book_id)
    except ValueError:
        print("Invalid book ID")
        return

    if library[library['ID'] == book_id].empty:
        print("Book not found")
        return

    book_title = library.loc[library['ID'] == book_id, 'Title'].values[0]
    confirm = MessageBox.askyesno("Confirm Delete", f"Are you sure you want to delete the book with title: {book_title}?")
    if not confirm:
        return

    library.drop(library[library['ID'] == book_id], inplace=True)
    # library.reset_index(drop=True, inplace=True)
    # library['ID'] = library  # Update the ID column to match the new index
    library.to_csv('books.csv', sep=';', index=False)
    MessageBox.showinfo("Success", "Book deleted successfully")
    # root.destroy()

