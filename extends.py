from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from libs._celery import celery_factory

db = SQLAlchemy()
# config sqlalchemy

ckeditor = CKEditor()
# config ckeditor

# config login_mgr
login_mgr = LoginManager()
login_mgr.login_view = "admin.login"
login_mgr.login_message_category = "warning"
login_mgr.login_message = "该页面需登录后访问，请先登录！"

csrf = CSRFProtect()

# WTF_CSRF_METHODS默认为["POST", "PUT", "PATCH", "DELETE"]


# celery
worker = celery_factory("worker")
beat = celery_factory("worker")
fast = celery_factory("fast")

print("*" * 10 + "extends.py ending" + "*" * 10)
