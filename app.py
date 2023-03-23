from flask_migrate import Migrate
from flask import Flask, render_template, jsonify, request
from extends import db, ckeditor, login_mgr, csrf
from views import admin, blog, user
from views.blog import old_function_api
from settings import CommonConf
from flask_wtf.csrf import CSRFError
import models


def create_app(*args, **kwargs):
    app = Flask("flask_blog", *args, **kwargs)
    app.config.from_object(CommonConf)
    register_exts(app)
    register_request_deal()
    register_api_class()
    register_bps(app)
    register_error(app)
    Migrate(app, db)

    print(app.config.get("SQLALCHEMY_DATABASE_URI"))

    return app


def register_exts(app):
    db.init_app(app)
    ckeditor.init_app(app)
    login_mgr.init_app(app)
    csrf.init_app(app)


def register_bps(app):
    app.register_blueprint(user.user_bp, url_prefix="/user")
    app.register_blueprint(blog.blog_bp, url_prefix="/blog")
    app.register_blueprint(admin.admin_bp, url_prefix="/admin")


def register_error(app):
    @app.errorhandler(CSRFError)
    def csrf_error_deal(e):
        # 用到csrf_protect的目前只有 del_art/del_cty两个ajax发送json的Post请求，
        # 此处改写错误处理，返回200的response，json供ajax解析显示错误信息
        return jsonify({"success": False, "msg": e.description})


def register_request_deal():
    import libs.RequestDeals


def register_api_class():
    blog.func.register_api()
    admin.func.register_api()


app_inst = create_app()


@app_inst.route("/")
def index():
    return render_template("index.html")


@app_inst.route("/test")
def test():
    a = models.Admin.query.get(1000)
    print(a)
    b = models.Admin.query.get("asd")
    print(b)
    c = models.Admin.query.get(-7)
    print(c)
    # return request.path
    return jsonify({"a": a, "b": b, "c": c})


if __name__ == "__main__":
    # 本地测试使用Flask应用自带的Web开发服务器，并开启调试模式
    app_inst.run(debug=True)
