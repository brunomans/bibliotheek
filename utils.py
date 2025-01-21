import pandas as pd
import requests
from isbnlib import meta 
import sys
import gc
import textwrap




def determine_next_id(library_ids):
    if not library_ids:
        return 0
    
    sorted_ids = sorted(library_ids)
    
    for expected_id in range(sorted_ids[0], sorted_ids[-1] + 1):
        if expected_id not in sorted_ids:
            return expected_id

    return sorted_ids[-1] + 1

def get_book_info(isbn):
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    response = requests.get(url)
    data = response.json()
    if data['totalItems'] == 0:
        for service in ['wiki', 'openl']:
                try:
                    new_data = meta(isbn=str(isbn), service=service)

                    if new_data:
                        title = new_data['Title']
                        authors = new_data['Authors']
                        publisher = new_data['Publisher']
                        print(f"Data found from {service}:")
                        print(f"Title: {title}")
                        print(f"Authors: {authors}")
                        print(f"Publisher: {publisher}")
                        return title, authors, publisher, None
                    else:
                        print(f"No data found from {service}")
                except Exception as e:
                    print(f"Error retrieving data from {service}: {e}")
            
        print('Nothing found')
        return None

    else:
        book = data['items'][0]['volumeInfo']
        title = book.get('title', None)
        authors = book.get('authors', None)
        publisher = book.get('publisher', None)
        # year = book['publishedDate'].dt.year

    if 'imageLinks' not in book:
        image = None
    else:
        image = book['imageLinks']['thumbnail']
    return title, authors, publisher, image


def check_garbage_collection(img):
    """Check if an image is still in memory by looking at its reference count."""
    ref_count = sys.getrefcount(img)
    print(f"Reference count of image: {ref_count}")
    
    gc.collect()  
    print(f"Garbage collected objects: {gc.garbage}")



def format_title(title, max_length=15):
    words = title.split()
    lines = []
    current_line = " "

    for word in words:
        if len(current_line) + len(word) + (1 if current_line else 0) <= max_length:
            if current_line:
                current_line += " "
            current_line += word
        else:
            if current_line:
                lines.append(current_line)
            current_line = " "
            
            while len(word) > max_length:
                lines.append(word[:max_length-1] + "-")
                word = word[max_length-1:]
            
            current_line = word

    if current_line:
        lines.append(current_line)

    return "\n  ".join(lines)
