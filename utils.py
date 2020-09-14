import json
import pandas as pd

def get_dataframe():
	data = pd.read_json('set1-en_us.json')
	data = data[['name', 'region', 'attack', 'cost', 'health', 'rarity']]
	return data.to_html()

if __name__ == '__main__':
	data = pd.read_json('set1-en_us.json')
	print(data.head())
	print(data.columns)