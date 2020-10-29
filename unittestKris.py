import unittest
import sqlalchemy
import sqlite3
from utils import getDeck

class databaseTests(unittest.TestCase):
    def test_addBlank(self):
        deck = getDeck('Test') # should create test deck, adds a game

        actual = []
        expected = ["Win/Loss", "Opponent Regions", "Opponent Champs"]

        # establishing connection
        connection = sqlite3.connect('card_data/stattracker.db')
        c = connection.cursor()
        with connection:
            check = c.execute("PRAGMA TABLE_INFO(Test)")
            for x in check:
                actual.append(x[1])
        self.assertEqual(actual, expected)

        # Deletes test deck when done
        with connection:
            c.execute("DROP TABLE Test")
if __name__ == '__main__':
    unittest.main()
