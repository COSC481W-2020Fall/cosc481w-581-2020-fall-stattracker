import unittest
import sqlalchemy
import sqlite3
from utils import getDeck, createUser, addUserDeck

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
        # if user exists - return True
        # if user does not exist = return False and add to db
        testUser = createUser('test') # create fake user that doesn't exist
        testUser2 = createUser('ryoumi') # try to create user that does exist

        # hardcoding the test
        self.assertEqual(testUser, False)

        # delete fake user
        connection = sqlite3.connect('card_data/usersdecks.db')
        c = connection.cursor()
        with connection:
            c.execute("DROP TABLE test")

        self.assertEqual(testUser2, True)

    def test_adduserDeck(self):
        testUser = createUser('testDeck') # creating fake user

        stats = ["Generic deck name", "CIBAIAYGAQDQQDYIAMESGKJNGM2DOPC4AEBAGCITKUAA"]
        addUserDeck('testDeck', stats) # 1
        stats = ["Second deck name", "CIBQCAIBA4AQEAICBMBAMBIIBMGREFA4EARC2OQAAEAQGBQO"]
        addUserDeck('testDeck', stats) # 2
        stats = ["Final deck name", "CICACAQEBIBACAIEEABAEAICA4CQCBAIDENTIOQCAEBACCQDAECCOMJVAIAQCAJKAEAQIGQ"]
        addUserDeck('testDeck', stats) # 3

        # since deck code is already added under "Second deck code" it shouldn't add this one
        stats = ["Check this out", "CIBQCAIBA4AQEAICBMBAMBIIBMGREFA4EARC2OQAAEAQGBQO"]
        addUserDeck('testDeck', stats) # 4

        # masking sure it adds to full deck stats if not exist
        stats = ["Dummy test", "TestTest"]
        addUserDeck('testDeck', stats) # 5

        connection = sqlite3.connect('card_data/usersdecks.db')
        c = connection.cursor()
        with connection:
            c.execute("SELECT count(*) FROM testDeck")
            deckCount = c.fetchone()[0]

            c.execute("DROP TABLE testDeck") # deleting added decks for testing

        masConnection = sqlite3.connect('card_data/stattracker.db')
        c = masConnection.cursor()
        with connection:
            c.execute("DROP TABLE TestTest") # deleting added decks for testing

        self.assertEqual(deckCount, 4) # the actual test portion

if __name__ == '__main__':
    unittest.main()
