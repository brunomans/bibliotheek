# Bibliotheek - Book Library Management System

This project is a Book Library Management System that allows users to scan ISBN barcodes, manually enter book details, and view the library's collection. The system uses a combination of Python libraries such as `tkinter` for the GUI, `pandas` for data manipulation, and `PIL` for image processing.

## Features

- **Add books**: Add books based on ISBN barcode or from a csv file with ISBN codes.
- **Scan ISBN Barcodes**: Automatically fetch book details using the ISBN barcode.
- **Manual Book Entry**: Manually enter book details if the ISBN is not found.
- **View Books**: Display books in a scrollable grid with images.
- **Switch Views**: Toggle between viewing books as images and in a DataFrame format.

### To be added
- **Loan**: If someone has borrowed your book it can be added.
- **Status**: Shows whether you have read the book.
- **Edit books**: Increase the edit possibilities.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/brunomans/bibliotheek.git
    cd bibliotheek
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Bieb**:
    - Run the [bieb.py](http://_vscodecontentref_/0) script to go to the main screen.
    - From here you can add a book, view all books, import a list of books, scan ISBNs, edit/delete books.

    ```sh
    python bieb.py
    ```

2. **Add Books**:
    - Run the [addBooks.py](http://_vscodecontentref_/1) script to add books to the library.
    - If the ISBN is not found, you will be prompted to manually enter the book details.

    ```sh
    python addBooks.py
    ```

3. **Scan ISBNs**:
    - Run the [scanISBN.py](http://_vscodecontentref_/2) script to scan ISBN barcodes and add books to the library.
    - Makes use of [ISBNScanner.py] (which is based on barcode_scanner.py by FaxanaduHacks (https://github.com/FaxanaduHacks/librarian))

    ```sh
    python scanISBN.py
    ```

4. **View Books**:
    - Run the [viewBooks.py](http://_vscodecontentref_/3) script to view the books in the library.
    - You can switch between viewing books as images and in a DataFrame format.

    ```sh
    python viewBooks.py
    ```
5. **Edit Books**:
    - Run the [editBooks.py](http://_vscodecontentref_/3) script to edit the books in the library.
    - You can switch between viewing books as images and in a DataFrame format.
    - Not finished

    ```sh
    python editBooks.py
    ```
6. **Import Books**:
    - Run the [addBooks.py](http://_vscodecontentref_/3) script to import books to the library.
    - Import a list of ISBNs to import the books.
    - Must be formatted with "ISBN" as a header and saved as a .CSV file.
    - Not finished.

    ```sh
    python addBooks.py
    ```

## File Structure

- [bieb.py](): Main script, run this to start from libraries maine page.
- [addBooks.py](http://_vscodecontentref_/3): Script to add books to the library, either by scanning ISBNs or manual entry.
- [scanISBN.py](http://_vscodecontentref_/4): Script to scan ISBN barcodes and add books to the library.
- [viewBooks.py](http://_vscodecontentref_/5): Script to view the books in the library.
- [editBooks.py](): Script to make changes to the books. ( This is not finished )
- [utils.py](http://_vscodecontentref_/6): Utility functions used across the project.
- [info.json](http://_vscodecontentref_/7): Configuration file containing library information.
- [books.csv](http://_vscodecontentref_/8): CSV file storing the library's book collection.
- [detected_barcodes.csv](http://_vscodecontentref_/8): CSV file temporarily storing the scanned ISBNs.
- [bookcover.jpg](): An image that is used and edited if no image has been found from the web.
- [lib.jpg](): An image containing the background for the library application.

## Dependencies

- `tkinter`: For creating the GUI.
- `pandas`: For data manipulation and CSV handling.
- `PIL` (Pillow): For image processing.
- `requests`: For fetching book images from URLs.
- `isbnlib`: For validating and fetching book details using ISBN.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- This project uses the `isbnlib` library for ISBN validation and fetching book details.
- The GUI is built using `tkinter`.
- Image processing is done using the `PIL` (Pillow) library.
