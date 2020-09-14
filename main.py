from flask import Flask, render_template, request, redirect
from utils import get_dataframe

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/deckbuilder', methods=['GET','POST'])
def deck_builder():
	if request.method == 'POST':
		if request.form.get('Home'):
			return redirect('/')
	elif request.method == 'GET':
		return render_template('deckbuilder.html', data=get_dataframe())

if __name__ == '__main__':
	app.run(debug=True)