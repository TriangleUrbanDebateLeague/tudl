from flask import session, request, g, flash, redirect, url_for
from functools import wraps

class roles:
    hours_approver = 1
    admin = 1

def require_login(f):
    @wraps(f)
    def _decorated(*args, **kwargs):
        if g.user is not None:
            return f(*args, **kwargs)
        else:
            flash("Please log in first.", "info")
            return redirect(url_for("account.login", next=request.path))
    return _decorated


def require_role(minimum_role):
    def _decorator(f):
        @wraps(f)
        def _decorated(*args, **kwargs):
            if g.user is not None:
                if g.user.role >= minimum_role:
                    return f(*args, **kwargs)
                else:
                    flash("You don't have permission to do that :(", "error")
                    return redirect(url_for("account.info"))
            else:
                flash("Please log in first.", "info")
                return redirect(url_for("account.login", next=request.path))
        return _decorated
    return _decorator
