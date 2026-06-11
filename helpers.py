from flask import session, redirect, render_template
from functools import wraps
import random


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def apology(message, code=400):
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def get_quote():
    quotes = [
        "Be Fucking Bored!",
        "Remember, You certainly wouldn't like to do stuff, at a point of time, but keep going, don't stop even if you want to, atleast do the bare minimum",
        "Aim for progress, no matter how minute it is, not perfection",
        "Perfection is never attained"
    ]
    return random.choice(quotes)
