# Legends of Runeterra StatTracker

A program for keeping track of the popularity of cards.

<h2 align="center">Prototype Description</h2>

- A user interface for the user to choose their options

	- Building and naming new decks

		- The user can build custom decks.

			- Users will add cards to the deck one at a time from a library of cards available from the [API](https://developer.riotgames.com/docs/lor).

			- The program will keep track of deck size and space left.

			- The program will monitor the deck for any errors with its structure including validity and size and will notify the user if errors become apparent.

			- The program will not let the user add cards that are out of the parameters of legal deck building.

			- The user can cancel to stop building their deck

			- The user can confirm the deck to save it.

		- Decks will be viewable in an inventory page for the user to browse and explore.

			- Existing decks can be edited to add or remove cards.

			- Decks can be deleted.

	- Save/restore deck(s)

		- The user can store their decks with reference to each card's information, and then restore the decks for later use

	- View stats

		- The user can choose a card from the API and view it's information/stats

- Database to hold card information

	- CSV

	- Holds card information that is valuable to the user

	- Database structured to make it easy to see which cards are more popular to use and what cards work well together

- Web interface

	- Built with flask

	- Simple to use without having to download any software

	- Accessible with any major web browser that the user has

	- 4 main pages:

		- Building a deck

		- Importing/exporting decks

		- Browsing card information

		- Viewing information/stats

- Card information

	- Name of the card

	- Costs

	- 'Stats'

	- Ratio of use in gameplay

	- win/loss percentage

	- Common cards used together
