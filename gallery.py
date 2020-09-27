import json
import html
import pandas as pd
from flask import render_template
from pandas.io.json import json_normalize

def g_home(cardcode):
	# get data
	df = pd.read_json('card_data/set1-en_us.json')

	if cardcode == None:
		# limit data to these fields
		df = df[['name', 'cardCode']]
		print(df)
		# render page and add json data as js variable
		jsondata = json.loads(df.to_json())
		return render_template('gallery/index.html', jsondata=jsondata)

	else:
		# limit data to these fields
		df = df[['name', 'assets', 'description', 'cardCode']]
		# find the row that matches the cardcode parameter
		df = df.loc[df['cardCode'] == cardcode]
		# extract the card information
		name = df.iloc[0]['name']
		image = df.iloc[0].assets[0]['fullAbsolutePath']
		description = df.iloc[0].description
		# render the page
		return render_template('gallery/card.html', name=name, image=image, description=description)

# https://stackoverflow.com/a/42264209/13157180
def make_clickable(val):
    return '<a href="/gallery/{}">Link</a>'.format(val,val)