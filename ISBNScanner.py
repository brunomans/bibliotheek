import cv2
from pyzbar import pyzbar
import os
import isbnlib
import time
import pandas as pd

class ISBNScanner:
    def __init__(self):
        self.detected_barcodes = []
        self.book_detected = False
        self.isbn_stored = False
        self.last_valid_isbn = None
        self.barcode_detected = False

    # def isbn_exists(self, isbn):
    #     df = pd.read_csv('isbns.csv', sep=';')
    #     return isbn in df['ISBN'].values

    # def store_isbn(self, isbn, frame):
    #     if self.isbn_exists(isbn):
    #         print('ISBN already exists')
    #         return False

    #     df = pd.read_csv('isbns.csv', sep=';')
    #     df = df.append({'ISBN': isbn}, ignore_index=True)
    #     df.to_csv('isbns.csv', index=False, sep=';')
    #     print('ISBN stored')

    #     self.save_capture(frame, isbn)
    #     return True

    def save_capture(self, frame, isbn):
        if not os.path.exists('captures'):
            os.makedirs('captures')
        cv2.imwrite(f'captures/{isbn}.png', frame)
        print('Capture saved')

    def capture_barcode(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()

            cv2.imshow('Barcode Scanner', frame)

            if not self.book_detected and not self.isbn_stored:
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    barcodeData = barcode.data.decode("utf-8")
                    self.barcode_detected = True
                    print('Barcode detected:', barcodeData)
                    if isbnlib.is_isbn13(barcodeData):
                        print('Valid ISBN:', barcodeData)
                        self.last_valid_isbn = barcodeData
                        self.detected_barcodes.append(barcodeData)  # Add barcode to list
                        self.book_detected = True
                        break

            if self.barcode_detected:
                self.book_detected = True
                self.isbn_stored = True
            else:
                self.book_detected = False
                self.isbn_stored = False

            if self.barcode_detected:
                print('Barcode detected')
                print("Last valid ISBN:", self.last_valid_isbn)
            # else:
            #     print('No barcode detected')

            self.barcode_detected = False

            if cv2.waitKey(1) in (ord('q'), 27):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.export_barcodes_to_csv()  # Export barcodes when exiting

    def is_valid_isbn(self, isbn):
        isbn = isbn.replace('-', '').replace(' ', '')
        return isbnlib.is_isbn13(isbn)

    def start_scanning(self):
        print("Starting barcode scanner - Press 'q' or 'esc' to quit")

        self.create_table()
        self.capture_barcode()

    def export_barcodes_to_csv(self):
        df = pd.DataFrame(self.detected_barcodes, columns=['ISBN'])
        df.drop_duplicates(subset='ISBN', keep='first', inplace=True)
        df.to_csv('detected_barcodes.csv', index=False)
        print('Barcodes exported to detected_barcodes.csv')
# if __name__ == '__main__':
#     scanner = ISBNScanner()
#     scanner.start_scanning()
