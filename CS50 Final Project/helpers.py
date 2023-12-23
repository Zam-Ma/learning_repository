import sqlite3
import re
from flask import redirect, render_template, session, g
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def pln(value):
    """Format value as PLN."""
    return f"{value:,.2f} zł"


def apology(message, code=400):
    """Render message as an apology to user."""

    return render_template("apology.html", message=message, code=code)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("portphel.db")
        g.db.row_factory = sqlite3.Row  # This allows accessing columns by name
        g.cursor = g.db.cursor()
    return g.db, g.cursor


def createDefaultCategories(user_id, db, cursor):
    defaultCategories = [
        "No category",
        "Fixed costs",
        "Groceries",
        "Car",
        "Medicine",
        "Entertainment",
        "Kids",
        "Other",
    ]
    for category in defaultCategories:
        cursor.execute(
            "INSERT INTO categories (user_id, category) VALUES (?, ?)",
            (user_id, category),
        )
    db.commit()


def validate(*args):
    if len(args) == 1:
        if not re.search(r"^.{1,100}$", args[0]):
            return False  # Invalid category name
        return True

    if len(args) == 2:
        # Check if beginDate is in the format YYYY-MM-DD
        if (
            not re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$", args[0])
            and args[0] != ""
        ):
            return False  # Invalid date format
        # Check if endDate is in the format YYYY-MM-DD
        if (
            not re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$", args[1])
            and args[1] != ""
        ):
            return False  # Invalid date format
        return True

    if len(args) == 4:
        # Check if title is between 1 and 100 characters
        if not re.search(r"^.{1,100}$", args[0]):
            return False  # Invalid title

        # Check if cost is a valid float with two decimal places and between 0 and 100000
        try:
            cost_float = float(args[1])
            if not (0 <= cost_float <= 100000):
                return False  # Invalid cost
        except ValueError:
            return False  # Invalid cost (not a valid float)

        # Check if category_id is a valid positive integer
        try:
            category_id_int = int(args[2])
            if not (category_id_int > 0):
                return False  # Invalid category_id
        except ValueError:
            return False  # Invalid category_id (not a valid integer)

        # Check if date is in the format YYYY-MM-DD
        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$", args[3]):
            return False  # Invalid date format

        # If everything is valid, return True
        return True


def clear(string):
    string = string.replace("--", "- ")
    return string
