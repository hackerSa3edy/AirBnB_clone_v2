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

from flask import Flask, render_template
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


@app.route("/c/<string:text>", strict_slashes=False)
def c_is_fun(text="") -> str:
    """
    A route function that returns a formatted string when the "/c/<text>" URL
    is accessed.

    Parameters:
        text (str): The text to be included in the returned string. Defaults
        to an empty string.

    Returns:
        str: A string in the format of "C <text>", where <text> is replaced by
        the input text with underscores replaced by spaces.
    """
    return f"C {text.replace('_', ' ')}"


@app.route("/python/", defaults={"text": "is_cool"})
@app.route("/python/<string:text>", strict_slashes=False)
def python_route(text) -> str:
    """
    A route function that returns a formatted string when the "/python/<text>"
    URL is accessed.

    Parameters:
        text (str): The text to be included in the returned string. Defaults
        to "is cool".

    Returns:
        str: A string in the format of "Python <text>", where <text> is
        replaced by the input text with underscores replaced by spaces.
    """
    return f"Python {text.replace('_', ' ')}"


@app.route("/number/<int:n>", strict_slashes=False)
def is_it_number(n) -> str:
    """
    A route function that returns a formatted string when the "/number/<n>"
    URL is accessed.

    Parameters:
        n (int): The integer to be included in the returned string.

    Returns:
        str: A string in the format of "<n> is a number", where <n> is
        replaced by the input integer.
    """
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_temp(n):
    """
    A route function that renders a template when the "/number_template/<n>" URL is accessed.

    Parameters:
        n (int): The integer to be passed to the template.

    Returns:
        render_template: A function that takes in the name of a template file and a variable number of keyword arguments, and returns a string with placeholders in the template file replaced with the appropriate values.
    """
    return render_template("5-number.html", number=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def odd_or_even(n):
    """
    A route function that renders a template when the "/number_odd_or_even/<n>" URL is accessed.

    Parameters:
        n (int): The integer to be passed to the template.

    Returns:
        render_template: A function that takes in the name of a template file and a variable number of keyword arguments, and returns a string with placeholders in the template file replaced with the appropriate values.
    """
    return render_template("6-number_odd_or_even.html", number=n)


if __name__ == '__main__':
    """
    The main entry point for the application.
    It starts the Flask development server at the host and port specified.
    """
    app.run("0.0.0.0", 5000)
