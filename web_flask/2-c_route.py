#!/usr/bin/python3
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


if __name__ == "__main__":
    print(__name__)
    app.run(host="0.0.0.0", port=5000)
