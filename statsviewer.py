from flask import render_template
import sqlite3
import pandas as pd

def sv_home():
	avoidTables = ['set', 'API']

	# get dataframe of db
	cnx = sqlite3.connect("card_data/stattracker.db")
	df = pd.read_sql_query("select name from sqlite_master where type = 'table'", cnx)

	# extract table names
	tableNames = []
	for index, row in df.iterrows():
		if row['name'] not in avoidTables:
			tableNames.append(row['name'])

	# get stats for first deck
	df = pd.read_sql_query("select * from " + tableNames[0], cnx)

	return render_template('statsviewer/index.html', data=df.to_json(), name=tableNames[0])

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