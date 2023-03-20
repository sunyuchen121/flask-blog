from flask import Blueprint

a = __name__
print(a)
user_bp = Blueprint("user", "user")

import views.user.func
