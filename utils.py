import json
import csv
import os
import pandas as pd
import sqlite3
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
	data = data.reset_index(drop=True)
	return data

# Converting json to csv file with WINRATE columns
def convertToCSV(importedFile, csvName):
	csv_file = pd.DataFrame(pd.read_json(importedFile))
	csv_file.to_csv(csvName, header = True)

	# converting that file so it's just the card codes
	csv_file = pd.read_csv(csvName, usecols=["cardCode"])
	csv_file["Wins"] = "0" # adding Wins columns
	csv_file["Losses"] = "0" # adding Losses columns
	csv_file.to_csv(csvName, header = True)

def createDatabase(filename):
	# define connection & cursor
	database = 'card_data/' + filename + '.db'
	connection = sqlite3.connect(database)
	return database

# For a clean and simple 'save this csv file as is to the database'
def importToDatabase(filename):
	file = 'card_data/' + filename + '.csv' # CSV file to import into database
	connection = sqlite3.connect('card_data/stattracker.db')

	# Reading csv file to database
	data = pd.read_csv(file)
	data.to_sql(filename, connection, if_exists='replace', index=False)
	os.remove(file)

def dataToDB(filename):
	file = "card_data/" + filename + ".xlsx"
	deckList = pd.read_excel(file, sheet_name=None)

	for x in deckList.keys():
		deckName = x
		temp = pd.read_excel(file, sheet_name=x)
		temp.to_csv('card_Data/' + x + '.csv', header=True)
		importToDatabase(deckName)

# Saving and appending decks to database, hardcoded to append 'card_data' and '.csv' to end of filename
# So you don't have to reference when calling method
def WINRATEtoDatase(filename, colUsed, colAdd):
	file = filename + '.csv'
	connection = sqlite3.connect('card_data/stattracker.db')

	# Saving the table with specified columns
	csvFile = pd.read_csv(file, usecols=colUsed)

	# If we decided we want to add a column(s)
	if len(colUsed) < 0:
		for x in colAdd:
			csvFile[x] = "0"

	# Saving table to database
	csvFile.to_sql(filename, connection, if_exists='replace', index=False)

if __name__ == '__main__':
	data = get_dataframe() # do not delete
