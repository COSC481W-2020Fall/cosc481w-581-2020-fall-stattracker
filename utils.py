import json
import pandas as pd
import glob

def get_dataframe():
	files = glob.glob('card_data/*.json')

	data = []
	for file in files:
		data.append(pd.read_json(file))

	data = pd.concat(data)
	data = data[['cardCode', 'name', 'region', 'attack', 'cost', 'health', 'rarity']]
	func = lambda x: False if 'T' in x[-2:] else True
	mask = data['cardCode'].apply(func)
	data = data[mask]
	return data
	
if __name__ == '__main__':
	data = get_dataframe()

	func = lambda x: False if 'T' in x[-2:] else True
	mask = data['cardCode'].apply(func)
	data = data[mask]
	print(len(data))
	print(data)