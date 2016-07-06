from .decorators import require_permission
from .models import Permission
from flask import Blueprint, current_app, render_template
from modules.account.models import Account

security = Blueprint("security", __name__, template_folder="templates", url_prefix="/security")

@security.route("/")
@require_permission("security", "access")
def security_index():
    modules = sorted(list(current_app.blueprints.keys()))
    return render_template("security/index.html", modules=modules)

@security.route("/query/all/")
@require_permission("security", "access")
def all_permissions():
    permissions = Permission.select(Permission, Account).join(Account)
    return render_template("security/permissions.html", header="All permissions", permissions=permissions)

@security.route("/query/module/<module>/")
@require_permission("security", "access")
def permissions_for_module(module):
    permissions = Permission.select(Permission, Account).where(Permission.module == module).join(Account)
    return render_template("security/permissions.html", header="Permissions for module: {}".format(module), permissions=permissions)

@security.route("/query/user/<int:uid>/")
@require_permission("security", "access")
def permissions_for_user(uid):
    account = Account.get(id=uid)
    permissions = account.permissions
    return render_template("security/permissions.html", header="Permissions for user: {}".format(account.full_name), permissions=permissions)
