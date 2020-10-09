from flask import Flask, render_template, request, redirect, url_for
from utils import get_dataframe
from gallery import g_home
import pandas as pd
import glob
import os
import numpy as np

app = Flask(__name__)

@app.route('/', methods =["GET","POST"])
def Home():
	if request.method == "POST":
		if request.form.get("Deck_Builder"):## Sends you to the Deck Builder Page
			return redirect("deckbuilder")
		if request.form.get("Card_Gallery"):## Sends you to the Card Gallery Page
			return redirect("gallery")
	else:
		return render_template("Home.html") 

decks = glob.glob('decks/*.csv')
dataFrame = get_dataframe()
cardList = dataFrame.to_html()

@app.route('/deckbuilder', methods=['GET','POST'])
def deck_builder():

	if request.method == 'POST': ## Gets some input from page

		if request.form.get('Home'): ## Redirect to home page
			return redirect('/')

		## Create new deck
		if request.form.get('deckName'):
			deckName = request.form['deckName']
			## Save deck and add to list of available decks
			columns = dataFrame.columns
			activeDeck = pd.DataFrame(columns=dataFrame.columns)
			activeDeck['wins'] = 0
			activeDeck['losses'] = 0
			path = f'decks/{deckName}.csv'
			activeDeck.to_csv(path)
			if path not in decks:
				decks.append(path)
				activeDeck = activeDeck.to_html()
			elif path in decks or not deckName:
				activeDeck = None

		## Select deck to view
		if request.form.get('selectDeck'):
			deckName = request.form['selectDeck']
			activeDeck = pd.read_csv(deckName)
			activeDeck = activeDeck.to_html()

		## Deletes deck
		if request.form.get('deleteDeck'):
			deckName = request.form['deleteDeck']
			os.remove(deckName)
			if deckName in decks:
				decks.remove(deckName)
			deckName = None
			activeDeck = None

		## Add card to deck
		if request.form.get('cardID'): ## Receive card id to add to deck
			cardID = request.form['cardID']
			row = dataFrame.loc[dataFrame['cardCode'] == cardID]

			deckName = request.form['selectDeck']
			## Write row to specified deck database
			activeDeck = pd.read_csv(deckName)
			numChampions = 0
			if len(activeDeck) > 0:
				counts = activeDeck['cardCode'].value_counts()
				rarity = activeDeck['rarity'].value_counts()
				if 'Champion' in rarity:
					numChampions = rarity['Champion']
				if cardID in counts:
					numCopies = counts[cardID]
				else:
					numCopies = 0
			else:
				numCopies = 0

			if row.iloc[0]['rarity'] == 'Champion' and numCopies < 3 and numChampions < 6 and len(activeDeck) < 40: ## Makes sure the deck fits the deckbuilding requirements.
				activeDeck = activeDeck.append(row, ignore_index=True)
			elif row.iloc[0]['rarity'] != 'Champion' and numCopies < 3 and len(activeDeck) < 40:
				activeDeck = activeDeck.append(row, ignore_index=True)
				
			activeDeck.to_csv(deckName, index=False)
			activeDeck = activeDeck.to_html()

		if request.form.get('cardIDDelete'):
			cardIDDelete = request.form['cardIDDelete']
			deckName = request.form['selectDeck']
			activeDeck = pd.read_csv(deckName)

			copysOfCard = activeDeck[activeDeck['cardCode'] == cardIDDelete].index
			cardToDelete = copysOfCard[np.random.randint(len(copysOfCard))]
			activeDeck.drop(cardToDelete, inplace=True)

			activeDeck.to_csv(deckName, index=False)
			activeDeck = activeDeck.to_html()

		if request.form.get('wins'):
			deckName = request.form['selectDeck']
			activeDeck = pd.read_csv(deckName)
			activeDeck['wins'] = int(request.form['wins'])

			activeDeck.to_csv(deckName, index=False)
			activeDeck = activeDeck.to_html()

		if request.form.get('losses'):
			deckName = request.form['selectDeck']
			activeDeck = pd.read_csv(deckName)
			activeDeck['losses'] = int(request.form['losses'])

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

@app.route('/gallery')
@app.route('/gallery/<cardcode>')
def gallery(cardcode = None):
	return g_home(cardcode)

if __name__ == '__main__':
	app.run(debug=True)