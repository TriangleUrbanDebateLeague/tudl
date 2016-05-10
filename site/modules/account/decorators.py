from flask import session, request, g, flash, redirect, url_for
from functools import wraps

def require_login(f):
    @wraps(f)
    def _decorated(*args, **kwargs):
        if g.user is not None:
            return f(*args, **kwargs)
        else:
            flash("Please log in first.", "info")
            return redirect(url_for("account.login", next=request.path))
    return _decorated
