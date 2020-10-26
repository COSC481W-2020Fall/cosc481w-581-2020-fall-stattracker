import unittest
import sqlalchemy
import sqlite3
from utils import addGameDB

class AppendUnitTest(unittest.TestCase):

	def test_appendDeck(self):
		actual = []
		expected = ['W', 'Ionia / Targon', 'Lee Sin']
		deck = addGameDB('CIBQCAIBA4AQEAICBMBAMBIIBMGREFA4EARC2OQAAEAQGBQO',expected)


		connection = sqlite3.connect('card_data/stattracker.db')
		c = connection.cursor()
		with connection:
			c.execute("""SELECT * FROM CIBQCAIBA4AQEAICBMBAMBIIBMGREFA4EARC2OQAAEAQGBQO""")
			records = c.fetchall()

		for x in records:
			actual.append(x)
		self.assertEqual(actual, expected)

		with connection:
				c.execute("DELETE FROM CIBQCAIBA4AQEAICBMBAMBIIBMGREFA4EARC2OQAAEAQGBQO ORDER BY  DESC LIMIT 1")



if __name__ == '__main__':
	unittest.main()

		