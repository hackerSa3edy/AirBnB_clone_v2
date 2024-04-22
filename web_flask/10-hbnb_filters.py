#!/usr/bin/python3
"""
This module defines a Flask web application that starts on 0.0.0.0
on port 5000.

Imports:
    Flask: Flask web server framework.
    render_template: Function to generate output from a template file.
    models: Module that contains the application models.

Routes:
    /hbnb_filters: Route that displays a HTML page with a list of all State
    and Amenity objects in the database.

Functions:
    clear_session(exception): Function that is called after each request to
    close the current SQLAlchemy session.
    hbnb_filters(): Function that is called when the /hbnb_filters route
    is accessed.

App:
    app: Instance of the Flask class.
"""

from flask import Flask, render_template
import models

app = Flask(__name__)


@app.teardown_appcontext
def clear_session(exception):
    """
    Closes the current SQLAlchemy session.

    This function is called after each request, regardless of whether an
    exception occurred during the request. The exception that occurred
    during the request, if any, is passed to this function.

    Parameters:
        exception (Exception): The exception that occurred during the
        request, if any.

    Returns: None
    """
    models.storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Renders a HTML page with a list of all State and Amenity objects in
    the database.

    The HTML page is found in the templates folder and is named
    10-hbnb_filters.html. The list of State and Amenity objects is passed to
    the template under the variable names states and amenities respectively.

    Parameters: None

    Returns:
        render_template: A function that takes in the name of a template file
        and a variable number of keyword arguments, and returns a string with
        placeholders in the template file replaced with the appropriate values.
    """
    state_objects = list(models.storage.all(models.State).values())
    amenity_objects = list(models.storage.all(models.Amenity).values())

    states = [
        {
            'name': state.name,
            'cities': [
                {
                    'city_name': city.name,
                        } for city in state.cities
                ]
            } for state in state_objects
        ]

    amenities = [
        {'name': amenity.name} for amenity in amenity_objects
    ]

    return render_template(
        "10-hbnb_filters.html",
        states=states,
        amenities=amenities
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
