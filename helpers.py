from flask import redirect, render_template, session
from functools import wraps

# handle login as member, adapted from CS50 finance
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return "Please login first", 403
        return f(*args, **kwargs)
    return decorated_function