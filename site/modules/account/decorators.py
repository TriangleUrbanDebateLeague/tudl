from flask import session, request
from functools import wraps

def require_login(f):
    @wraps(f)
    def _decorated(*args, **kwargs):
        if "logged_in" not in session or not session["logged_in"]:
            flash("Please log in first.", "info")
            return redirect(url_for("account.login", next=request.path))
        return f(*args, **kwargs)
