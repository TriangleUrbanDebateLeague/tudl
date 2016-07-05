from .localutils import has_permission
from flask import g, request, flash
from functools import wraps

def require_permission(module, permission):
    def _decorator(f):
        @wraps(f)
        def _decorated(*args, **kwargs):
            if g.user is None:
                flash("Please log in first.", "info")
                return redirect(url_for("account.login", next=request.path))

            if not has_permission(g.user, module, permission):
                flash("You don't have permission to do that :(", "error")
                return redirect(url_for("account.info"))

            return f(*args, **kwargs)
        return _decorated
    return _decorator
