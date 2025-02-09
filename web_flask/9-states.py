#!/usr/bin/python3
"""Starts a flask web app"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """diplays a list of states and their cities"""
    states = storage.all("State")
    return render_template('9-states.html', state=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """diplays a list of states"""
    states = storage.all("State")
    for state in states.values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template('9-states.html')


@app.teardown_appcontext
def close_db(Exception=None):
    """closes sqlalchemy session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
