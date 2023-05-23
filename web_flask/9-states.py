#!/usr/bin/python3
"""Python script that starts a F;ask Web Application"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


# app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.route('/states', defaults={'id': None}, strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_cities(id):
    states = storage.all(State).values()
    valid = 0
    if id is None:
        valid = 1
    else:
        for state in states:
            if state.id == id:
                valid = 1
                break
    return render_template('9-states.html', states=states, valid=valid, id=id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
