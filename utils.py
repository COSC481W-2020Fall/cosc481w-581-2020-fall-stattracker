import json
import pandas as pd

def get_dataframe():
	data = pd.read_json('card_data/set1-en_us.json')
	data = data[['cardCode', 'name', 'region', 'attack', 'cost', 'health', 'rarity']]
	return data
	
if __name__ == '__main__':
	data = pd.read_json('card_data/set1-en_us.json')
	print(data.head())
	print(data.columns)
	counts = data['cardCode'].value_counts()
	print(counts)
	if '01IO040' in counts:
		print(True)
	else:
		print(False)