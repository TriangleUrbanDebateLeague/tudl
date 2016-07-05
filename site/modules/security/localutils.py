from .models import Permission

def has_permission(user, module, permission):
    q = Permission.select().where(Permission.account == g.user & Permission.module == module & Permission.permission == permission)
    return q.count() > 0
