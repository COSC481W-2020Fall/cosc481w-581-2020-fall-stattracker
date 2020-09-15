from flask import Flask, render_template, request, redirect
from utils import get_dataframe
import pandas as pd
import glob

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/deckbuilder', methods=['GET','POST'])
def deck_builder():
	dataFrame = get_dataframe()
	html_code = dataFrame.to_html()
	decks = glob.glob('decks/*.csv')

	if request.method == 'POST': ## Gets some input from page

		if request.form.get('Home'): ## Redirect to home page
			return redirect('/')

		if request.form.get('deckName'): ## Create empty csv file for deck info
			deckName = request.form['deckName']

			## Save deck and add to list of available decks
			deck = pd.DataFrame()
			path = f'decks/{deckName}.csv'
			deck.to_csv(path)
			if path not in decks:
				decks.append(path)

		if request.form.get('cardID'): ## Receive card id to add to deck
			deckName = 'mydeck'
			# print(request.form['selectDeck'])
			cardID = request.form['cardID']
			row = dataFrame.loc[dataFrame['cardCode'] == cardID]

			## Write row to specified deck database
			path = f'decks/{deckName}.csv'
			deck = pd.read_csv(path)
			deck = deck.append(row, ignore_index=True)
			deck.to_csv(path, index=False)

		return render_template(
			'deckbuilder.html',
			data=html_code,
			deck=deck.to_html(),
			decks=decks)

	elif request.method == 'GET': ## If initial reqeust of page, display it
		return render_template(
			'deckbuilder.html',
			data=html_code,
			deck=None,
			decks=decks)

if __name__ == '__main__':
	app.run(debug=True)