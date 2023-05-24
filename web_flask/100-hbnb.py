#!/usr/bin/python3
"""Python script that starts a F;ask Web Application"""

from flask import Flask
from flask import render_template
from markupsafe import Markup
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place


app = Flask(__name__)


# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb_places():
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()

    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places, br=Markup('<br>'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
