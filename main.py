from flask import Flask
from flask import render_template

from utils import get_dataframe

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/deckbuilder')
def deck_builder():
	return get_dataframe()

if __name__ == '__main__':
	app.run(debug=True)