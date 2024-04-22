#!/usr/bin/python3
"""
This module defines a Flask web application that starts on 0.0.0.0
on port 5000.

Imports:
    Flask: Flask web server framework.
    render_template: Function to generate output from a template file.
    models: Module that contains the application models.

Routes:
    /states: Route that displays a HTML page with a list of all State objects
    in the database.
    /states/<id>: Route that displays a HTML page with a specific State object
    and its associated City objects in the database.

Functions:
    clear_session(exception): Function that is called after each request to
    close the current SQLAlchemy session.
    cities(id): Function that is called when the /states or /states/<id>
    route is accessed.

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
    exception occurred during the request. The exception that occurred during
    the request, if any, is passed to this function.

    Parameters:
        exception (Exception): The exception that occurred during the request,
        if any.

    Returns: None
    """
    models.storage.close()

@app.route('/states', strict_slashes=False, defaults={'id': None})
@app.route('/states/<id>', strict_slashes=False)
def cities(id):
    """
    Renders a HTML page with a list of all State objects or a specific State
    object and its associated City objects in the database.

    The HTML page is found in the templates folder and is named 9-states.html.
    The list of State objects or the specific State object and its associated
    City objects is passed to the template under the variable name data.

    Parameters:
        id (str): The id of the specific State object to display. If this is
        None, all State objects are displayed.

    Returns:
        render_template: A function that takes in the name of a template file
        and a variable number of keyword arguments, and returns a string with
        placeholders in the template file replaced with the appropriate values.
    """
    data = {'states': None, 'state': None}
    if id is not None:
        state = models.storage.all(models.State).get(f'State.{id}')
        if state is not None:
            state = {
                'id': state.id,
                'name': state.name,
                'cities': [
                    {
                        'city_id': city.id,
                        'city_name': city.name
                        } for city in state.cities
                    ]
                }
            data.update({'state': state})
    else:
        states = list(models.storage.all(models.State).values())
        states = [
            {
                'id': state.id,
                'name': state.name,
                } for state in states
            ]
        data.update({'states': states})

    return render_template(
        "9-states.html",
        data=data,
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
