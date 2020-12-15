from flask import render_template
import sqlite3
import pandas as pd
from lor_deckcodes import LoRDeck, CardCodeAndCount

def sv_home():
	avoidTables = ['set', 'API']

	# get dataframe of db
	cnx = sqlite3.connect("card_data/stattracker.db")
	df = pd.read_sql_query("select name from sqlite_master where type = 'table'", cnx)

	# extract deck names
	deckNames = []
	for index, row in df.iterrows():
		if row['name'] not in avoidTables:
			deckNames.append(row['name'])
	
	framesToConcat = []
	for i in range(len(deckNames)):

		# get stats for deck
		unnamedDf = pd.read_sql_query("select * from " + deckNames[i], cnx)

		# add deck name to data
		# https://stackoverflow.com/a/53236864/13157180
		nameCol = []
		for j in range(len(unnamedDf.index)):
			nameCol.append(deckNames[i])
		nameDf = pd.DataFrame(nameCol, columns=['Deck Name'])
		unnamedDf.append(nameDf)

		# add frames to array
		framesToConcat.append(pd.concat([unnamedDf, nameDf], axis=1))

	# make df out of array
	deckData = pd.concat(framesToConcat)
	deckData.reset_index(drop=True, inplace=True) # reset indexes

	# make df of cards in each deck
	CardDataCardCode = []
	CardDataDeckCode = []
	for deckName in deckNames:
		try:
			deck = LoRDeck.from_deckcode(deckName)
			for card in deck.cards:
				CardDataCardCode.append(str(card)[2:]) # trim quantity
				CardDataDeckCode.append(deckName)
		except ValueError:
			# Invalid deck code, skip
			pass
	cardData = pd.DataFrame(data={'Deck Name':CardDataDeckCode, 'Card Code':CardDataCardCode})

	return render_template('statsviewer/index.html', deckData=deckData.to_json(), cardData=cardData.to_json())

def count_wins(df):
	count = 0
	for row in df['Win/Loss']:
		if row == 'W':
			count += 1
	return count

def count_losses(df):
	count = 0
	for row in df['Win/Loss']:
		if row == 'L':
			count += 1
	return count

def win_avg(df):
	return count_wins(df) / len(df.index)