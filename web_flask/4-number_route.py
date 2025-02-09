#!/usr/bin/python
"""
Script starts a flask web app

Routes:
    /: displays 'Hello HBNB!'
    /hbnb: diplays 'HBNB'
    /c/<text>: display “C ”, followed by the value of the text variable
    /python/<text>: display “Python ”, followed by the value of the text variable
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Return 'Hello HBNB!' for the root route."""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Return 'HBNB' for the /hbnb route."""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Return 'C ' followed by text with underscores replaced by spaces."""
    return f"C {text.replace('_', ' ')}"


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """Return 'Python ' followed by text with underscores replaced by spaces."""
    return f"Python {text.replace('_', ' ')}"

@app.route('/number/<int:n>', strict_slashes=False)
def number_n(n):
    """Displays 'n is a number' if n is an int"""
    return f"{n} is a number"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
