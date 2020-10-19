import json
import html
import pandas as pd
import glob
from flask import render_template
from pandas.io.json import json_normalize

def g_home(cardcode):
	# get data
	# df = pd.read_json('card_data/set1-en_us.json')
	filenames = glob.glob('card_data/*.json')
	dfs = []
	for filename in filenames:
		dfs.append(pd.read_json(filename))
	df = pd.concat(dfs, ignore_index=True)

	if cardcode == None:
		# limit data to these fields
		df = df[['name', 'cardCode']].sort_values('name')
		print(df)
		# render page and add json data as js variable
		jsondata = json.loads(df.to_json())
		return render_template('gallery/index.html', jsondata=jsondata)

	else:
		# limit data to these fields
		df = df[['name', 'assets', 'description', 'cardCode', 'cost', 'type']]
		# find the row that matches the cardcode parameter
		df = df.loc[df['cardCode'] == cardcode]
		# extract the card information
		name = df.iloc[0]['name']
		image = df.iloc[0].assets[0]['fullAbsolutePath']
		description = df.iloc[0].description
		cost = df.iloc[0]['cost']
		cardtype = df.iloc[0]['type']
		# render the page
		return render_template('gallery/card.html', name=name, image=image, description=description, cost=cost, cardtype=cardtype)

# https://stackoverflow.com/a/42264209/13157180
def make_clickable(val):
    return '<a href="/gallery/{}">Link</a>'.format(val,val)