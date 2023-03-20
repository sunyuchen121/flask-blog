from flask import Blueprint

admin_bp = Blueprint("admin", "admin")
a = __name__
print(a)


import views.admin.func
