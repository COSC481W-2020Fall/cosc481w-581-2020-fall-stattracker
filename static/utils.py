import json
import csv
import os
import pandas as pd
import sqlite3
import glob
import sqlalchemy
from lor_deckcodes import LoRDeck, CardCodeAndCount

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

# Simple 'save csv file to the database'
def importToDatabase(filename):
	file = 'card_data/' + filename + '.csv' # CSV file to import into database
	connection = sqlite3.connect('card_data/stattracker.db')

	# Reading csv file to database
	data = pd.read_csv(file)
	del data["DeckCode"] # deletes the column with the deck code
	del data["Unnamed: 0"] # deletes that extra column at the beginning
	data.to_sql(filename, connection, if_exists='replace', index=False)
	os.remove(file)

# Adds a list of decks from excel file to databse
# Changes the names of the decks to the deck codes
def addDeckDB(filename):
	file = "card_data/" + filename + ".xlsx"
	deckList = pd.read_excel(file, sheet_name=None)

	for x in deckList.keys():
		temp = pd.read_excel(file, sheet_name=x)
		deckName = temp.iloc[0]['DeckCode']
		temp.to_csv('card_Data/' + deckName + '.csv', header=True)
		importToDatabase(deckName)

# adds stats from a game to database
# deckName = deck code
# gameStates = an array with
#  - Win/Losses - W or L
#  - Opponent Regions - String (Region1 / Region2)
#  - Opponent Champs - String (Champion1 / Champion2 / Champion3 / ...)
def addGameDB(deckname, gameStats):
	connection = sqlite3.connect('card_data/stattracker.db')
	c = connection.cursor()

	outcome = gameStats [0]
	regions = gameStats [1]
	champions = gameStats [2]
	with connection:
		c.execute("CREATE TABLE IF NOT EXISTS " + deckname + " ('Win/Loss', 'Opponent Regions', 'Opponent Champs')")
		c.execute("INSERT INTO " + deckname + " VALUES(?, ?, ?)", (outcome, regions, champions))

# Grabs a deck from the database and returns it
def getDeck(deckname):
	connection = sqlite3.connect('card_data/stattracker.db')
	c = connection.cursor()
	with connection:
		c.execute("CREATE TABLE IF NOT EXISTS " + deckname + " ('Win/Loss', 'Opponent Regions', 'Opponent Champs')")
		c.execute("SELECT * FROM " + deckname)
		return c.fetchall()

# checks if user exists
# if not adds them to database and returns true
# if yes, returns false
def createUserDB(name):
	# create an ID
	connection = sqlite3.connect('card_data/usersdecks.db')
	c = connection = cursor()

	with connection:
		c.execute("SELECT test FROM sqlite_master WHERE type='table' AND name='table_name'")
		if c.fetchone()[0]==1:
			return True # user already exists, so throw an error
		else:
			c.execute("CREATE TABLE " + name + " ('DeckName, DeckCode')") # adds users table to db
			return False

def get_champs():
	data = get_dataframe()
	return data[data['rarity'] == 'Champion']['name'].to_list()

## Takes in a valid card code and returns a pandas dataframe with
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

if __name__ == '__main__':
	data = get_dataframe() # do not delete

	# getDeck("temp")
