#!/usr/bin/python3
"""
This is a simple Flask application that serves a single route.

Imports:
    Flask (from flask): The main class that all the functionality of Flask
    depends upon.

Global variables:
    app (Flask): The main Flask application instance.

Functions:
    hello_hbnb: The function to be called when the root URL ("/") is
    accessed. It returns a string.
"""

from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb() -> str:
    """
    A route function that returns a string when the root URL ("/") is accessed.

    Parameters: None

    Returns:
        str: The string "Hello HBNB!"
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb() -> str:
    """
    A route function that returns a string when the "/hbnb" URL is accessed.

    Parameters: None

    Returns:
        str: The string "HBNB"
    """
    return "HBNB"


if __name__ == '__main__':
    """
    The main entry point for the application.
    It starts the Flask development server at the host and port specified.
    """
    app.run("0.0.0.0", 5000)
