import unittest
from io import StringIO
import os

from book import Book, scan_book
from misc import trace, dd, Multiple, safe_unlink


mock_file = StringIO("""

Arma virumque cano Trojae qui primus ab oris

aeneas quamquam et sociis dare tempus humandis


""")

class TestBook(unittest.TestCase):

    maxDiff = None

    def test_basics(self):
        safe_unlink('db/TestBook.db')
        output = StringIO()
        book = scan_book('Test Book', mock_file, output)
        self.assertEqual(book.dbname, 'db/TestBook')
        self.assertEqual(len(book), 2)
        self.assertEqual(len(book[1].scans), 7)
        self.assertTrue(0 not in book)
        self.assertTrue(1 in book)
        self.assertTrue(2 in book)
        self.assertTrue(3 not in book)

        self.assertEqual(output.getvalue(),
"""1. arma virumque cano trojae qui primus ab oris (7 scans)
2. aeneas quamquam et sociis dare tempus humandis (0 scans)
""")
        # This might break because we can't always tell what shelve will
        # name the database file.
        #os.unlink('db/TestBook.db')
