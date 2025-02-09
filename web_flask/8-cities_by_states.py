#!/usr/bin/python3
"""Starts a flask web app"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """diplays a list of states and their cities"""
    states = storage.all("State")
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def close_db(Exception=None):
    """closes sqlalchemy session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
