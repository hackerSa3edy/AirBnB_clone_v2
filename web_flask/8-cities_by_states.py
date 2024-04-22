#!/usr/bin/python3
"""
This module defines a Flask web application that starts on 0.0.0.0
on port 5000.

Imports:
    Flask: Flask web server framework.
    render_template: Function to generate output from a template file.
    models: Module that contains the application models.

Routes:
    /cities_by_states: Route that displays a HTML page with a list of all
    State objects and their associated City objects in the database.

Functions:
    clear_session(exception): Function that is called after each request
    to close the current SQLAlchemy session.
    cities_by_states(): Function that is called when the
    /cities_by_states route is accessed.

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
        exception (Exception): The exception that occurred during the request,
        if any.

    Returns: None
    """
    models.storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Renders a HTML page with a list of all State objects and their associated
    City objects in the database.

    The HTML page is found in the templates folder and is named
    8-cities_by_states.html. The list of State objects and their associated
    City objects is passed to the template under the variable name
    cities_by_state.

    Parameters: None

    Returns:
        render_template: A function that takes in the name of a template file
        and a variable number of keyword arguments, and returns a string with
        placeholders in the template file replaced with the appropriate values.
    """
    states = list(models.storage.all(models.State).values())
    all = [
        {
            'id': state.id,
            'name': state.name,
            'cities': [
                {
                    'city_id': city.id,
                    'city_name': city.name
                        } for city in state.cities
                ]
            } for state in states
        ]

    return render_template(
        "8-cities_by_states.html",
        # "7-states_list.html",
        cities_by_state=all
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
