import pandas as pd
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests
from io import BytesIO
from utils import *
import json

with open('info.json','r') as f:
    data = json.load(f)

library_name = data['Library_name']

def fetch_image(row):
    image_url = row['Image']
    try:
        if image_url is None or pd.isnull(image_url) or image_url == 'nan':

            title = format_title(row['Title'])
            photo = Image.open('bookcover.jpg')
            draw = ImageDraw.Draw(photo)
            font_size = 40
            font = ImageFont.truetype("arial.ttf", font_size)
            text_width, text_height = photo.size
            width, height = photo.size
            x = 0
            y = 0
            draw.text((x, y), title, fill='White', font=font)
            photo = photo.resize((60, 90), Image.LANCZOS)
            return ImageTk.PhotoImage(photo)
        else:
            response = requests.get(image_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((60, 90), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None


def View(root, library):
    image_references = []

    def show_images():
        for widget in labelFrame.winfo_children():
            widget.destroy()


        canvas = Canvas(labelFrame, bg='#2e2e2e')  
        scrollbar_y = Scrollbar(labelFrame, orient=VERTICAL, command=canvas.yview)
        scrollbar_x = Scrollbar(labelFrame, orient=HORIZONTAL, command=canvas.xview)
        scrollable_frame = Frame(canvas, bg='#2e2e2e') 

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor=NW)
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        def update_images():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            labelFrame.update_idletasks()
            columns = max(1, labelFrame.winfo_width() // 100)  

            for index, row in library.iterrows():
                photo = fetch_image(row)  
                if photo:
                    label = Label(scrollable_frame, image=photo, bg='#2e2e2e')  
                    label.image = photo  
                    label.grid(row=index // columns, column=index % columns, padx=10, pady=10)
                    image_references.append(photo)  

        update_images()
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        labelFrame.bind("<Configure>", lambda event: update_images())

    def show_treeview():
        for widget in labelFrame.winfo_children():
            widget.destroy()

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

    show_treeview()

    switchBtn = Button(top, text="Switch to Images", bg='#f7f1e3', fg='black', command=lambda: show_images() if switchBtn['text'] == "Switch to Images" else show_treeview())
    switchBtn.place(relx=0.3, rely=0.9, relwidth=0.4, relheight=0.08)

    def toggle_button_text():
        if switchBtn['text'] == "Switch to Images":
            switchBtn['text'] = "Switch to DataFrame"
        else:
            switchBtn['text'] = "Switch to Images"

    switchBtn.config(command=lambda: [toggle_button_text(), show_images() if switchBtn['text'] == "Switch to DataFrame" else show_treeview()])

    top.mainloop()
