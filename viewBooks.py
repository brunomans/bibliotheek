import pandas as pd
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO
import sys
import gc
import json

with open('info.json','r') as f:
    data = json.load(f)

library_name = data['Library_name']

def fetch_image(row):
    image_url = row['Image']  # Get the image URL from the DataFrame
    print(f"Fetching image: {image_url}")
    if image_url is None or pd.isnull(image_url) or image_url == 'nan': 
        print("No image URL found")
        title = row['Title']
        photo = Image.open('bookcover.jpg')
        # write the title of the book on the image
        draw = ImageDraw.Draw(photo)
        # draw in the center of the image
        text_width, text_height = photo.size
        width, height = photo.size
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        draw.text((x, y), title, fill='White')





        photo = photo.resize((60, 90), Image.LANCZOS)  # Resize the image
        return ImageTk.PhotoImage(photo)  # Convert image to a format Tkinter can use
    else:
        """Fetch the image from the URL and return a PhotoImage object."""
        try:
            response = requests.get(image_url)
            photo = Image.open(BytesIO(response.content))
            photo = photo.resize((60, 90), Image.LANCZOS)  # Resize the image
            photo = ImageTk.PhotoImage(photo)  # Convert image to a format Tkinter can use

            return photo
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None

def check_garbage_collection(img):
    """Check if an image is still in memory by looking at its reference count."""
    # Get the reference count of the object
    ref_count = sys.getrefcount(img)
    print(f"Reference count of image: {ref_count}")
    
    # Use garbage collector to check if the image is still in memory
    gc.collect()  # Forcing garbage collection
    print(f"Garbage collected objects: {gc.garbage}")

def View(root, library):
    
    # List to hold image references
    image_references = []

    def show_images():
        # Clear the frame
        for widget in labelFrame.winfo_children():
            widget.destroy()

        # Display images in the frame
        for index, row in library.iterrows():
            photo = fetch_image(row)  # Fetch image from URL
            # check_garbage_collection(photo)
            
            if photo:
                label = Label(labelFrame, image=photo)
                label.image = photo  # Store reference to image in the label widget
                label.pack(side='left', padx=10, pady=10)

                image_references.append(photo)  # Keep reference in the list

                # Check if the image is garbage collected
                

    def show_treeview():
        # Clear the frame
        for widget in labelFrame.winfo_children():
            widget.destroy()

        # Display the Treeview in the frame
        tree = ttk.Treeview(labelFrame, columns=(1,2,3,4,5), show="headings", height="5")
        tree.pack(side='left', expand=True, fill='both')

        tree.heading(1, text="ID")
        tree.heading(2, text="ISBN")
        tree.heading(3, text="Title")
        tree.heading(4, text="Author")
        tree.heading(5, text="Owner")

        tree.column(1, width=50)
        tree.column(2, width=100)
        tree.column(3, width=200)
        tree.column(4, width=100)
        tree.column(5, width=100)

        scroll = ttk.Scrollbar(labelFrame, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scroll.set)

        for index, row in library.iterrows():
            tree.insert("", 'end', values=(row['ID'],row['ISBN'], row['Title'], row['Authors'], row['Owner']))

    top = Toplevel(root)
    top.title(library_name)
    top.minsize(width=400, height=400)
    top.geometry("600x400")

    canvas = Canvas(top)
    canvas.config(bg="#ff6e40")
    canvas.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(top, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = Label(headingFrame1, text="View Books", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(top, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    # Initial view - images
    show_images()

    # Button to switch views
    switchBtn = Button(top, text="Switch View", bg='#f7f1e3', fg='black', command=lambda: show_treeview() if switchBtn['text'] == "Switch View" else show_images())
    switchBtn.place(relx=0.3, rely=0.9, relwidth=0.4, relheight=0.08)

    def toggle_button_text():
        if switchBtn['text'] == "Switch View":
            switchBtn['text'] = "Switch to Images"
        else:
            switchBtn['text'] = "Switch View"

    switchBtn.config(command=lambda: [toggle_button_text(), show_treeview() if switchBtn['text'] == "Switch to Images" else show_images()])

    top.mainloop()

