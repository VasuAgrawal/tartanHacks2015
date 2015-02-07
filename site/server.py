from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route('/')
def main():
    return render_template("create.html")

@app.route('/submit', methods=['POST'])
def create_game():
   print request.form['organizer']
   print request.form['participants']
   return "woo!"

if __name__ == '__main__':
        app.run()
