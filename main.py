from flask import Flask, render_template, request, redirect
from utils import get_dataframe
import pandas as pd
import glob
import os


app = Flask(__name__)

@app.route('/', methods =["GET","POST"])
def Home():
	if request.method == "POST":
		print("Hello World")
		if request.form.get("Deck_Builder"):
			print("This is line 11")
			return redirect("deckbuilder")
		if request.form.get("Card_Gallery"):
			return redirect("gallery")
	else:
		return render_template("Home.html") 


@app.route('/deckbuilder', methods=['GET','POST'])
def deck_builder():
	dataFrame = get_dataframe()
	cardList = dataFrame.to_html()
	decks = glob.glob('decks/*.csv')

	if request.method == 'POST': ## Gets some input from page

		if request.form.get('Home'): ## Redirect to home page
			return redirect('/')

		## Create new deck
		if request.form.get('deckName'):
			deckName = request.form['deckName']
			## Save deck and add to list of available decks
			activeDeck = pd.DataFrame()
			path = f'decks/{deckName}.csv'
			if path not in decks:
				activeDeck.to_csv(path)
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
			activeDeck = activeDeck.append(row, ignore_index=True)
			activeDeck.to_csv(deckName, index=False)
			activeDeck = activeDeck.to_html()

		## Renders webpage after post request
		return render_template(
			'deckbuilder.html',
			deckName=deckName,
			cardList=cardList,
			activeDeck=activeDeck,
			decks=decks)

	## Initial page request
	elif request.method == 'GET':
		return render_template(
			'deckbuilder.html',
			deckName=None,
			cardList=cardList,
			activeDeck=None,
			decks=decks)

if __name__ == '__main__':
	app.run(debug=True)