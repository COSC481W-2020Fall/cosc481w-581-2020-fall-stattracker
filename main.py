from flask import Flask, render_template, request, redirect, url_for, flash
from utils import get_dataframe, get_champs, addGameDB, buildFromCode
from gallery import g_home
from statsviewer import sv_home
import pandas as pd
import glob
import os
import numpy as np

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/home', methods =["GET","POST"])
def Home():
	if request.method == "POST":
		if request.form.get("Deck_Builder"):## Sends you to the Deck Builder Page
			return redirect("deckbuilder")
		if request.form.get("Card_Gallery"):## Sends you to the Card Gallery Page
			return redirect("gallery")
		if request.form.get("dataInputPage"):## Sends you to the Data Input Page
			return redirect("datainput")
	else:
		return render_template("Home.html")
## Start code for dataInputPage
decks = glob.glob('decks/*.csv')
champs = get_champs()
champs.append('None')

@app.route('/datainput', methods=['GET','POST'])
def data_input():
	if request.method == 'POST':
		code = request.form['cardCode']
		outcome = request.form['wl']
		regions = request.form['region1']
		if request.form['region'] not in regions:
			regions += " / " + request.form['region']
		# Adding the champions
		strCh = " "
		theChamps = " "
		for x in range(6):
			strCh = "champ" + str(x+1)
			if request.form[strCh] != "None":
				if len(theChamps) == 1:
					theChamps = request.form[strCh]
				elif request.form[strCh] not in theChamps:
					theChamps += " / " + request.form[strCh]
		stats = [outcome, regions, theChamps]
		addGameDB(code, stats)
		if outcome == "Win":
			flash("Congratulations on your victory!")
			return redirect(request.url)
		else:
			flash("Better luck next time...")
			return redirect(request.url)
	return render_template(
		'dataInputPage/dataInputPage.html',
		decks=decks,
		champs=champs)


## Start code for deckbuilder
decks = glob.glob('decks/*.csv')
dataFrame = get_dataframe()
cardList = dataFrame.to_html()

@app.route('/deckbuilder', methods=['GET','POST'])
def deck_builder():

	if request.method == 'POST': ## Gets some input from page

		if request.form.get('Home'): ## Redirect to home page
			return redirect('/')

		if request.form.get('fromCode'):
			deckName = request.form['deckName']
			code = request.form['deckCode']
			activeDeck = buildFromCode(code)
			path = f'decks/{deckName}.csv'
			activeDeck.to_csv(path)
			if path not in decks:
				decks.append(path)
				activeDeck = activeDeck.to_html()
			elif path in decks or not deckName:
				activeDeck = None

		## Create new deck
		if not request.form.get('fromCode') and request.form.get('deckName'):
			deckName = request.form['deckName']
			## Save deck and add to list of available decks
			columns = dataFrame.columns
			activeDeck = pd.DataFrame(columns=dataFrame.columns)
			activeDeck['count'] = None
			path = f'decks/{deckName}.csv'
			activeDeck.to_csv(path)
			if path not in decks:
				decks.append(path)
				activeDeck = activeDeck.to_html()
			elif path in decks or not deckName:
				activeDeck = None

		## Select deck to view
		if request.form.get('actions') == 'viewDeck':
			deckName = request.form['selectDeck']
			activeDeck = pd.read_csv(deckName)
			activeDeck = activeDeck.to_html()

		## Deletes deck
		if request.form.get('actions') == 'deleteDeck':
			deckName = request.form['selectDeck']
			os.remove(deckName)
			if deckName in decks:
				decks.remove(deckName)
			deckName = None
			activeDeck = None

		## Add card to deck
		# if request.form.get('actions') == 'addCard':
		# 	## Receive card id to add to deck
		# 	cardID = request.form['cardID']
		# 	row = dataFrame.loc[dataFrame['cardCode'] == cardID]
		# 	row = row.reset_index(drop=True)
		# 	row.loc[0, 'count'] = 1
		# 	isChamp = row.loc[0, 'rarity'] == 'Champion'

		# 	deckName = request.form['selectDeck']
		# 	activeDeck = pd.read_csv(deckName)

		# 	if cardID in list(activeDeck['cardCode']):
		# 		numCopies = activeDeck[activeDeck['cardCode'] == cardID].loc[0,'count']
		# 	else:
		# 		numCopies = 0

		# 	rarity = activeDeck['rarity'].value_counts()
		# 	if 'Champion' in rarity:
		# 		numChampions = rarity['Champion']
		# 	else:
		# 		numChampions = 0

		# 	if len(activeDeck) < 40:
		# 		if numCopies == 0:
		# 			activeDeck = activeDeck.append(row, ignore_index=True)
		# 			 # ((isChamp and numChampions < 6) or not isChamp)
		# 		elif 0 < numCopies < 3:
		# 			activeDeck.loc[activeDeck['cardCode'] == cardID, 'count'] += 1
					 
		# 	activeDeck.to_csv(deckName, index=False)
		# 	activeDeck = activeDeck.to_html()

		## Add card to deck
		if request.form.get('actions') == 'addCard': ## Receive card id to add to deck
			cardID = request.form['cardID']
			row = dataFrame.loc[dataFrame['cardCode'] == cardID]
			row = row.reset_index(drop=True)
			row.loc[0, 'count'] = 1
			isChamp = row.iloc[0]['rarity'] == 'Champion'

			deckName = request.form['selectDeck']
			## Write row to specified deck database
			activeDeck = pd.read_csv(deckName)

			if len(activeDeck) > 0:
				rarity = activeDeck['rarity'].value_counts()
				mask = (activeDeck['rarity'] == 'Champion')
				numChampions = sum(mask * activeDeck['count'])

				if cardID in list(activeDeck['cardCode']):
					numCopies = activeDeck.loc[activeDeck['cardCode'] == cardID, 'count'].item()
				else:
					numCopies = 0
			else:
				numCopies = 0
				numChampions = 0

			if numCopies == 0:
				activeDeck = activeDeck.append(row, ignore_index=True)
			elif isChamp and numCopies < 3 and numChampions < 5 and len(activeDeck) < 40:
				activeDeck.loc[activeDeck['cardCode'] == cardID, 'count'] += 1
			elif not isChamp and numCopies < 3 and len(activeDeck) < 40:
				activeDeck.loc[activeDeck['cardCode'] == cardID, 'count'] += 1

			activeDeck.to_csv(deckName, index=False)
			activeDeck = activeDeck.to_html()

		## Delete card
		if request.form.get('actions') == 'deleteCard':
			cardIDDelete = request.form['cardID']
			deckName = request.form['selectDeck']
			activeDeck = pd.read_csv(deckName)

			if cardIDDelete in list(activeDeck['cardCode']):
				numCopies = activeDeck.loc[activeDeck['cardCode'] == cardIDDelete, 'count'].item()
				if numCopies > 1:
					activeDeck.loc[activeDeck['cardCode'] == cardIDDelete, 'count'] -= 1
				else:
					activeDeck.drop(activeDeck[activeDeck['cardCode'] == cardIDDelete].index, inplace=True)

			activeDeck.to_csv(deckName, index=False)
			activeDeck = activeDeck.to_html()

		## Renders webpage after post request
		return render_template(
			'deckbuilder/deckbuilder.html',
			deckName=deckName,
			cardList=cardList,
			activeDeck=activeDeck,
			decks=decks)

	## Initial page request
	elif request.method == 'GET':
		return render_template(
			'deckbuilder/deckbuilder.html',
			deckName=None,
			cardList=cardList,
			activeDeck=None,
			decks=decks)
## End code for deckbuilder

@app.route('/gallery')
@app.route('/gallery/<cardcode>')
def gallery(cardcode = None):
	return g_home(cardcode)

@app.route('/statsviewer')
def statsviewer():
	return sv_home()

if __name__ == '__main__':
	app.run()
