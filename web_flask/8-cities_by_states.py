#!/usr/bin/python3
"""Python script that starts a F;ask Web Application"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_state():
    states = storage.all(State).values()

    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=sorted_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
