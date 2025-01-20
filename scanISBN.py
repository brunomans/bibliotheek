from ISBNScanner import ISBNScanner
from addBooks import get_book_info
import json
import pandas as pd
from utils import *

with open('info.json','r') as f:
    data = json.load(f)

# library_name = data['Library_name']
main_owner = data['Owner']

def scan_isbn(library):
    scanner = ISBNScanner()
    scanner.capture_barcode()

    scanned_df = pd.read_csv('detected_barcodes.csv', sep=';')

    for isbn in scanned_df['ISBN']:
        book_info = get_book_info(isbn)
        if book_info is None:
            print("Book not found")
            continue
        id = determine_next_id(library.ID.to_list())
        title, authors, publisher, image = book_info
        print(title, authors, publisher, image)
        library.loc[len(library)] = [id, isbn, title, authors, publisher, main_owner, image]
        library.drop_duplicates(subset='ISBN', keep='first', inplace=True)

        print("Book added successfully")

    library.to_csv('books.csv', sep=';', index=False)