from ISBNScanner import ISBNScanner
from addBooks import get_book_info, get_manual_book_info
import json
import pandas as pd
from utils import *
import tkinter as tk

with open('info.json', 'r') as f:
    data = json.load(f)

main_owner = data['Owner']

def scan_isbn(library):
    def add_book_to_library(manual_info):
        book_info = (manual_info['title'], [manual_info['authors']], manual_info['publisher'], None)
        isbn = manual_info['isbn']
        id = determine_next_id(library.ID.to_list())
        title, authors, publisher, image = book_info
        print(title, authors, publisher, main_owner, image)
        library.loc[len(library)] = [id, isbn, title, authors, publisher, main_owner, image]
        library.drop_duplicates(subset='ISBN', keep='first', inplace=True)
        library.to_csv('books.csv', sep=';', index=False)
        print("Book added successfully")

    scanner = ISBNScanner()
    scanner.capture_barcode()

    scanned_df = pd.read_csv('detected_barcodes.csv', sep=';')
    none_books = []
    
    for isbn in scanned_df['ISBN']:
        book_info = get_book_info(isbn)
        if book_info is None:
            none_books.append(isbn)
            print(none_books)
        else:
            id = determine_next_id(library.ID.to_list())
            title, authors, publisher, image = book_info
            print(title, authors, publisher, image)
            library.loc[len(library)] = [id, isbn, title, authors, publisher, main_owner, image]
            library.drop_duplicates(subset='ISBN', keep='first', inplace=True)
            print("Book added successfully")

    # Function to handle manual entry pop-ups sequentially
    def process_next_manual_entry(index=0):
        if index < len(none_books):
            isbn = none_books[index]
            print(f"Book with ISBN {isbn} not found. Please enter the details manually.")
            
            def callback(manual_info):
                if manual_info:
                    add_book_to_library(manual_info)
                process_next_manual_entry(index + 1)  # Proceed to next book after handling current

            get_manual_book_info(prefill_isbn=isbn, callback=callback)

    # Start processing manual entries
    process_next_manual_entry()

    library.to_csv('books.csv', sep=';', index=False)

