import json
import pandas as pd
from flask import render_template
from pandas.io.json import json_normalize

def g_home(cardcode):
	df = pd.read_json('card_data/set1-en_us.json')
	df = df[['name', 'assets', 'description', 'cardCode']]

	if cardcode == None:
		return render_template('gallery/index.html')
	else:
		df = df.loc[df['cardCode'] == cardcode]
		name = df.iloc[0]['name']
		image = df.iloc[0].assets[0]['fullAbsolutePath']
		description = df.iloc[0].description
		return render_template('gallery/card.html', name=name, image=image, description=description)
