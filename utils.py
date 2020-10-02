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
	func = lambda x: False if 'T' in x[-3:] else True
	mask = data['cardCode'].apply(func)
	data = data[mask]

	## This will be changed to grab the wins and losses from database
	data['winrate'] = 0
	return data
	
if __name__ == '__main__':
	data = get_dataframe()