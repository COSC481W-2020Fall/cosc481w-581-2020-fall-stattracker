import json
import csv
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

# Converting json to csv file
def convertToCSV(importedFile, csvName):
	csv_file = pd.DataFrame(pd.read_json(importedFile))
	csv_file.to_csv(csvName, header = True)

	# converting that file so it's just the card codes
	csv_file = pd.read_csv(csvName, usecols=["cardCode"])
	csv_file["Wins"] = "0" # adding Wins columns
	csv_file["Losses"] = "0" # adding Losses columns
	csv_file.to_csv(csvName, header = True)

if __name__ == '__main__':
	data = get_dataframe()
	# commenting this out - but I'm leaving this in here in case
	# we want to reference it for use with the decks for whatever reason
	# files = glob.glob('card_data/*.json')
	# for file in files:
	#	convertToCSV(file, 'card_data/set.csv')
