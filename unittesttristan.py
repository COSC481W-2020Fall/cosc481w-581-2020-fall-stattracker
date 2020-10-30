import unittest
from utils import buildFromCode
from lor_deckcodes import LoRDeck, CardCodeAndCount
from utils import get_dataframe

class DeckBuilderTests(unittest.TestCase):
	"""docstring for DeckBuilderTests"""

	def test_buildFromCode(self):
		deck = get_dataframe()
		
		testDeck = deck['cardCode'].value_counts().to_dict()
		f = lambda key, value: str(value) + ':' + key

		cardList = []
		for key, value in zip(testDeck.keys(), testDeck.values()):
			cardList.append(f(key, value))

		testDeck = LoRDeck(cardList)
		code = testDeck.encode()
		testDataframe = buildFromCode(code)

		valid = deck['cardCode'].unique().tolist()
		test = testDataframe['cardCode'].unique().tolist()

		valid.sort()
		test.sort()

		for x, y in zip(valid, test):
			self.assertEqual(x, y)

if __name__ == '__main__':
	unittest.main()