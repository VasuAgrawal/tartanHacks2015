from flask import Flask
from flask import render_template
from flask import request
import flask
app = Flask(__name__)

import cardsgame
import thread

flask.gameStarted = False

def create_game(organizer, participants):
    game = cardsgame.GameInstance(organizer, participants)
    thread.start_new_thread(game.run, ())

@app.route('/')
def main():
    return render_template("create.html")

@app.route('/submit', methods=['POST'])
def submit():
    if not flask.gameStarted:
        create_game(request.form['organizer'], request.form['participants'])
        flask.gameStarted = True
    return render_template("success.html")

if __name__ == '__main__':
    # flask.gameStarted = False
    app.run(debug = True)

