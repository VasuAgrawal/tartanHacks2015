from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

import cardsgame

def create_game(organizers, participants):
    print organizers
    print participants

@app.route('/')
def main():
    return render_template("create.html")

@app.route('/submit', methods=['POST'])
def submit():
    create_game(request.form['organizer'], request.form['participants'])
    return render_template("success.html")

if __name__ == '__main__':
        app.run()

