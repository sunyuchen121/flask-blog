from flask import Blueprint

blog_bp = Blueprint("blog", "blog")

import views.blog.func
