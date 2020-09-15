import json
import pandas as pd

def get_dataframe():
	data = pd.read_json('card_data/set1-en_us.json')
	data = data[['cardCode', 'name', 'region', 'attack', 'cost', 'health', 'keywords']]
	return data

if __name__ == '__main__':
	data = pd.read_json('card_data/set1-en_us.json')
	print(data.head())
	print(data.columns)