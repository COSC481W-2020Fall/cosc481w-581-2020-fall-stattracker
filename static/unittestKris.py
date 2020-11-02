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

    def test_addUser(self):
        # creating a fake user
        testUser = createUser('test') # returns whether it was added or not

        # establishing connection to database
        connection = sqlite3.connect('card_data/usersdecks.db')
        c = connection.cursor()

        with connection:
            # checking if table exists
            c.execute("SELECT test FROM sqlite_master WHERE type='table' AND name='table_name'")
            actual = c.fetchone()[0]==1

        self.assertEqual(testUser, actual)

        # deleting fake user
        with connection:
            c.execute("DROP TABLE test")

if __name__ == '__main__':
    unittest.main()
