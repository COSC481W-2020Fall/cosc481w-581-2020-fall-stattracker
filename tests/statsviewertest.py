# fix import pathing https://stackoverflow.com/a/16985066/13157180
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end of fix

from statsviewer import count_wins, count_losses, win_avg
import unittest
import pandas as pd

class TestStatsMethods(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		data = {
			'Win/Loss': ['W', 'L', 'W'],
			'Opponent Regions': ['Ionia / Targon', 'Noxus / Demacia', 'Freljord / Shadow Isles'],
			'Opponent Champs': ['Lee Sin', 'Vladimir', 'Tryndamere / Trundle']
		}
		columns = ['Win/Loss', 'Opponent Regions', 'Opponent Champs']
		cls.df = pd.DataFrame(data, columns)
		# print(df)

	def test_countwins(self):
		self.assertEqual(count_wins(self.df), 2)

	def test_countlosses(self):
		self.assertEqual(count_losses(self.df), 1)

	def test_countavg(self):
		self.assertEqual(win_avg(self.df), 2/3)

if __name__ == '__main__':
	unittest.main()