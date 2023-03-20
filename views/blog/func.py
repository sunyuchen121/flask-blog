import collections
import time

from views.blog import blog_bp
from models import Article, Category, Comment
from forms import ArticleForm, CategoryForm, CommentForm, ReplyForm
from flask_login import login_required, current_user
from flask import render_template, url_for, redirect, request, g, abort, flash
import itertools
from utils import update_attr, PageController
from libs.Decorator import permission_decorator, login_user_permission_decorator
from libs.EntryViews import EntryView


class ArticleView(EntryView):
    decorators = [login_user_permission_decorator(Article, ('index', 'read'))]
    GET_DEFAULT_FUNC = "default_process"
    MODEL = Article
    FORM = ArticleForm
    DEL_SHOW_KEY = "title"

    def default_process(self, *args, **kwargs):
        if kwargs.get("number"):
            article = self.get_data(kwargs.get("number"))
            form_data = {
                "title": article.title,
                "desc": article.desc,
                "body": article.body,
                "category": article.category_id,
                "number": article.id,
                "op": "edit"
            }
        else:
            article = self.model()
            form_data = {"op": "create"}
        self.form_.process(data=form_data)

        return render_template("blog_add.html", form_=self.form_, article=article)

    def read_process(self, *args, **kwargs):
        number = kwargs.get("number")
        article = self.get_data(number)
        if not article:
            abort(404)
        # 因为有外键约束，所以按照create_time排序结果，也可以保证 parent在前 child在后
        comments_all = Comment.query.filter_by(article_id=number).order_by(Comment.create_time.asc()).all()
        # todo relationship优化！！！
        comments = collections.defaultdict(lambda: {"parent": None, "child": []})
        for comment in comments_all:
            if not (comment.parent_id or comment.root_id):
                comments[comment.id]["parent"] = comment
            else:
                comments[comment.root_id]["child"].append(comment)

        return render_template("blog_read.html", article=article, comments=comments.values(),
                               comment_form=CommentForm(),
                               reply_form=ReplyForm())

    def index_process(self, *args, **kwargs):
        page_index, page_size = g.d_page_index, g.d_page_size
        articles = self.query.order_by(Article.create_time.desc()).paginate(page=page_index, per_page=page_size)

        categories = Category.query.all()
        return render_template("blog_list.html", articles=PageController(articles), categories=categories, hot_arts=[],
                               hot_auths=[])

    def create_data(self):
        if self.form_.validate_on_submit():
            info = self.model_data
            # SQLAlchemy中的BaseQuery对象上有一个方法update
            # article.update(info)
            # update_attr(article, info)
            self.create(info)
            flash(f"《{self.data.get('title')}》 创建成功！")

        self.flash_form_error()
        return redirect(url_for("blog.admin"))

    def edit_data(self):
        number = self.data.get("number")
        if self.form_.validate_on_submit():
            info = self.model_data
            update_res = self.update(number, info)
            if update_res is False:
                return self.json_resp(False, "未找到该文章！")

            flash(f"《{update_res.title}》更新成功！")

        self.flash_form_error()
        return redirect(url_for("blog.admin"))

    @property
    def model_data(self):
        info = {
            "title": self.form_.title.data,
            "desc": self.form_.desc.data,
            "body": self.form_.body.data,
            "category_id": self.form_.category.data,
            "creator_id": current_user.id
        }
        return info


class CategoryView(EntryView):
    # 等于 login_required(permission_decorator(Category)(func))
    # 装饰器加载顺序按列表中的顺序，Inner闭包执行顺序与列表中顺序相反
    decorators = [login_user_permission_decorator(Category)]
    MODEL = Category
    FORM = CategoryForm
    DEL_SHOW_KEY = "category"

    def get(self, number=None):
        page_index, page_size = g.d_page_index, g.d_page_size
        categories = PageController(self.model.get_own(order=True).paginate(page=page_index, per_page=page_size))
        self.form_.process(data={"user_email": current_user.email, "op": "create"})
        return render_template("blog_category.html", form_=self.form_, categories=categories)

    def create_data(self):
        if self.form_.validate_on_submit():
            data = {
                "category": self.data.get('name'),
                "creator_id": current_user.id
            }
            self.create(data)
            flash(f"{data.get('category')}：新增成功！")
        self.flash_form_error()
        return redirect(url_for("blog.category"))


def register_api():
    # Article MethodView
    blog_bp.add_url_rule("/article_add", view_func=ArticleView.as_view("article_add"), methods=["GET"])
    blog_bp.add_url_rule("/article_edit/<int:number>", view_func=ArticleView.as_view("article_edit"), methods=["GET"])
    blog_bp.add_url_rule("/article_post", view_func=ArticleView.as_view("article_post"), methods=["POST"])
    blog_bp.add_url_rule("/index", view_func=ArticleView.as_view("index"), methods=["GET"])
    blog_bp.add_url_rule("/read/<int:number>", view_func=ArticleView.as_view("read"), methods=["GET"])

    # Category MethodView
    blog_bp.add_url_rule("/category", view_func=CategoryView.as_view("category"), methods=["GET"])
    blog_bp.add_url_rule("/category_post", view_func=CategoryView.as_view("category_post"), methods=["POST"])
