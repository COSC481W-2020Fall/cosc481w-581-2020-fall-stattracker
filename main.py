from flask import Flask, render_template
from utils import get_dataframe
from gallery import g_home

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/deckbuilder')
def deck_builder():
	return get_dataframe()

@app.route('/gallery')
@app.route('/gallery/<cardcode>')
def gallery(cardcode = None):
	return g_home(cardcode)

if __name__ == '__main__':
	app.run(debug=True)