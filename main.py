from flask import Flask, render_template, request, redirect
from utils import get_dataframe


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


@app.route('/deckbuilder')
def deck_builder():
	return get_dataframe()

if __name__ == '__main__':
	app.run(debug=True)