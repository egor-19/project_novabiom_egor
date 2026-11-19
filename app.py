from flask import Flask 

app = Flask(__name__)

@app.route("/")
def print_first_text():
    return 'начальная страница!!!'