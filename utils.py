import pandas as pd
import requests
from isbnlib import meta 





def determine_next_id(library_ids):
    if not library_ids:
        return 0
    
    # Sort the IDs to find gaps
    sorted_ids = sorted(library_ids)
    
    # Check for gaps in the sequence
    for expected_id in range(sorted_ids[0], sorted_ids[-1] + 1):
        if expected_id not in sorted_ids:
            return expected_id

    # If no gaps, return max ID + 1
    return sorted_ids[-1] + 1

def get_book_info(isbn):
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    response = requests.get(url)
    data = response.json()
    # print(data)
    if data['totalItems'] == 0:
        # if no error new_data will be a dictionary with the book info else return None
        for service in ['wiki', 'openl']:
                try:
                    new_data = meta(isbn=isbn, service=service)

                    if new_data:
                        title = new_data['Title']
                        authors = new_data['Authors']
                        publisher = new_data['Publisher']
                        print(f"Data found from {service}:")
                        print(f"Title: {title}")
                        print(f"Authors: {authors}")
                        print(f"Publisher: {publisher}")
                        return new_data
                    else:
                        print(f"No data found from {service}")
                except Exception as e:
                    print(f"Error retrieving data from {service}: {e}")
            
            # If all services return nothing
        print('Nothing found')
        return None

    else:
        book = data['items'][0]['volumeInfo']
        title = book['title']
        authors = book['authors']
        publisher = book['publisher']
        # year = book['publishedDate'].dt.year
    # if no image set nan
    if 'imageLinks' not in book:
        image = None
    else:
        image = book['imageLinks']['thumbnail']
    return title, authors, publisher, image
# library = pd.read_csv('books.csv', sep=';')

# print(determine_next_id(library['ID'].to_list()))  # 3