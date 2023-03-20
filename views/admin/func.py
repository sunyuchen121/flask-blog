import flask
import itertools
from views.admin import admin_bp
from forms import LoginForm, RegisterForm
from flask import render_template, redirect, flash, url_for, jsonify, request, abort, typing as ft
from models import Admin
from flask_login import login_user, logout_user, current_user, login_required
from extends import db, login_mgr
from utils import redirect_back
from libs.EntryViews import EntryView
from libs.Decorator import permission_decorator


# @admin_bp.route("/register", methods=["POST", "GET"])
# def register():
#     form_ = RegisterForm()
#     if form_.validate_on_submit():
#         email = form_.data["email"]
#         if Admin.query.filter_by(email=email).first():
#             flash(f"{email}已经注册，请直接登录！")
#             return redirect(url_for("admin.register"))
#         # 注册用户默认非管理员 && 活跃状态
#         form_.data.update({
#             "is_active": True,
#             "_is_super": False
#         })
#         db.session.add(Admin(email=email, name=form_.data["username"], password=form_.data["password"],
#                              gender=form_.data["gender"], age=form_.data["age"]))
#         db.session.commit()
#         flash(f"注册成功：{email}")
#         return redirect(url_for("admin.login"))
#     if form_.errors:
#         flash('\n'.join(itertools.chain(*form_.errors.values())))
#     return render_template("register.html", form_=form_)
#
#
# @admin_bp.route("/login", methods=["POST", "GET"])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for("blog.index"))
#
#     form_ = LoginForm()
#     if form_.validate_on_submit():
#         email, password, remember = form_.data["email"], form_.data["password"], form_.data["remember"]
#         user = Admin.query.filter_by(email=email).first()
#         if not user:
#             flash(f"未找到邮箱：{email}，请先注册！")
#             return redirect(url_for("admin.login"))
#         if not user.validate_password(password):
#             flash(f"密码错误！")
#             return redirect(url_for("admin.login"))
#         login_user(user, remember)
#         return redirect_back()
#     if form_.errors:
#         flash('\n'.join(itertools.chain(*form_.errors.values())))
#
#     return render_template("login.html", form_=form_)
#
#
# @admin_bp.route("logout", methods=["POST"])
# def logout():
#     if current_user.is_authenticated is False:
#         return flask.jsonify({
#             "success": False,
#             "msg": "用户当前未登录！"
#         })
#     logout_user()
#     return render_template(url_for("index"))


class LoginView(EntryView):
    MODEL = Admin
    FORM = LoginForm
    ALLOW_OP = ("login", "logout")

    def get(self, number=None):
        if current_user.is_authenticated:
            return redirect(url_for("blog.index"))
        return render_template("login.html", form_=self.form_)

    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for("blog.index"))
        return super(LoginView, self).post()

    def login_data(self):
        if self.form_.validate_on_submit():
            email, remember = self.data.get("email"), self.data.get("remember")
            user = self.filter_dict(email=email).first()
            login_user(user, remember)
            return redirect_back()
        self.flash_form_error()
        return render_template("login.html", form_=self.form_)

    def logout_data(self):
        if current_user.is_authenticated is False:
            return self.json_resp(False, "用户当前未登录！")
        logout_user()
        return redirect(url_for("admin.login"))


class RegisterView(EntryView):
    MODEL = Admin
    FORM = RegisterForm
    ALLOW_OP = ("register",)

    def get(self, number=None):
        return render_template("register.html", form_=self.form_)

    def register_data(self):
        if self.form_.validate_on_submit():
            email = self.data.get("email")
            if self.filter_dict(email=email).first():
                flash(f"{email}已经注册，请直接登录！")
                return redirect(url_for("admin.register"))
            self.create({
                "email": email,
                "name": self.data.get("username"),
                "password": self.data.get("password"),
                "gender": self.data.get("gender"),
                "age": self.data.get("age")
            })

            flash(f"注册成功：{email}")
            return redirect(url_for("admin.login"))
        self.flash_form_error()
        return render_template("register.html", form_=self.form_)


def register_api():
    admin_bp.add_url_rule("/register", view_func=RegisterView.as_view("register"), methods=["POST", "GET"])
    admin_bp.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=["POST", "GET"])
    admin_bp.add_url_rule("/logout", view_func=LoginView.as_view("logout"), methods=["POST"])
