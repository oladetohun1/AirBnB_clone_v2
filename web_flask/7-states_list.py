#!/usr/bin/python3
"""Python script that starts a F;ask Web Application"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/state_list', strict_slashes=False)
def states_list():
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardown_db():
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
