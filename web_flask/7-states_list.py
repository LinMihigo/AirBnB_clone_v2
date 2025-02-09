#!/usr/bin/python3
"""Starts a flask web app"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """diplays a list of states"""
    states_obj = storage.all("State")
    return render_template('7-states_list.html', states_obj=states_obj)


@app.teardown_appcontext
def close_db(Exception=None):
    """closes sqlalchemy session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
