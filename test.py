from lor_deckcodes import LoRDeck, CardCodeAndCount
from utils import get_dataframe
import pandas as pd

def buildFromCode(code):
	data = get_dataframe()
	deck = LoRDeck.from_deckcode(code)

	codes = [(card.card_code, card.count) for card in deck.cards]

	newDeck = pd.DataFrame(columns=data.columns)

	for cardCode, count in codes:
		for _ in range(count):
			row = data.loc[data['cardCode'] == cardCode]
			newDeck = newDeck.append(row, ignore_index=True)
	return newDeck

deck = buildFromCode('CEBAIAIFB4WDANQIAEAQGDAUDAQSIJZUAIAQCBIFAEAQCBAA')
print(deck)