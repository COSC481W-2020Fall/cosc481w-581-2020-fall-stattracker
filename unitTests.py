import unittest
from utils import buildFromCode

class DeckBuilderTests(unittest.TestCase):
	"""docstring for DeckBuilderTests"""

	def test_buildFromCode(self):
		code = 'CEBAIAIFB4WDANQIAEAQGDAUDAQSIJZUAIAQCBIFAEAQCBAA'
		deck = buildFromCode(code)
		self.assertEqual(len(deck), 40)

if __name__ == '__main__':
	unittest.main()