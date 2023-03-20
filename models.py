import functools, operator

from extends import db
import sqlalchemy as sa
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask import request, jsonify


class Admin(db.Model, UserMixin):
    """
    is_authenticated
    is_active
    is_anonymous
    get_id()
    """
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    desc = db.Column(db.String(50))
    gender = db.Column(db.String(2))
    age = db.Column(db.Integer)
    password_hash = db.Column(db.String(200))
    site_title = db.Column(db.String(50))
    site_subtitle = db.Column(db.String(50))
    about = db.Column(db.Text)
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)

    _is_super = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # # 密码操作可通过init或@password.setter两种方式写入
    # # 不能直接传入password_hash，必须通过模型类的方法进行加密
    # def __init__(self, **kwargs):
    #     if "password_hash" in kwargs:
    #         raise AttributeError("该属性不可写入！")
    #     if "password" in kwargs and kwargs["password"]:
    #         kwargs["password_hash"] = generate_password_hash(kwargs.get("password"))
    #     else:
    #         raise AttributeError("密码不能为空！")
    #     super(Admin, self).__init__(**kwargs)

    @property
    def password(self):
        return "unknown!"

    @password.setter
    def password(self, value):
        if not value:
            raise AttributeError("密码不能为空！")
        self.password_hash = generate_password_hash(value)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(10), unique=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    @classmethod
    def get_own(cls, order=False):
        ctys = Category.query
        if not current_user._is_super:
            ctys = ctys.filter_by(creator_id=current_user.id)
        return ctys if not order else ctys.order_by(cls.create_time.desc())


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    desc = db.Column(db.String(100))
    body = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now)

    @classmethod
    def get_own(cls):
        arts = Article.query
        if not current_user._is_super:
            arts = arts.filter_by(creator_id=current_user.id)
        return arts


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    body = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    # 评论审核后边再做，暂时默认评论全部通过审核
    is_passed = db.Column(db.Boolean, default=True)
    # 评论根节点，若本身为根节点，则为空
    root_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    # 评论直接父级，若本身为根节点，则为空
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    passed_time = db.Column(db.DateTime, default=datetime.datetime.now)

    # todo relationship替换！！！
    @property
    def author(self):
        return Admin.query.filter(Admin.id == self.author_id).first()

    @property
    def parent_info(self):
        return Comment.query.filter_by(id=self.parent_id).first()


def data_role(cls, id_key="number", role_col="author_id"):
    user_id, is_super = current_user.id, current_user._is_super
    if not is_super:
        data_id = request.form.get(id_key)
        data_role_id = getattr(cls.query.get(data_id), role_col)
        return False if data_role_id != user_id else True
    return True


ArticleRole = functools.partial(data_role, cls=Article)
CategoryRole = functools.partial(data_role, cls=Category)
