import collections

from views.blog import blog_bp
from models import Article, Category, Comment
from forms import ArticleForm, CategoryForm, CommentForm, ReplyForm
from flask_login import login_required, current_user
from flask import render_template, url_for, redirect, request, g, jsonify, flash
from extends import db
import itertools
from utils import update_attr, PageController
from libs.Decorator import permission_decorator, login_user_permission_decorator
from libs.EntryViews import EntryView


# @blog_bp.route("/index")
# @login_required
# def index():
#     page_index, page_size = g.d_page_index, g.d_page_size
#     articles = Article.query.order_by(Article.create_time.desc()).paginate(page=page_index, per_page=page_size)
#
#     categories = Category.query.all()
#     return render_template("blog_list.html", articles=PageController(articles), categories=categories, hot_arts=[],
#                            hot_auths=[])


# @blog_bp.route("/read")
# @blog_bp.route("/read/<int:number>")
# @login_required
# def read(number=1):
#     article = Article.query.get(number)
#     # 因为有外键约束，所以按照create_time排序结果，也可以保证 parent在前 child在后
#     comments_all = Comment.query.filter_by(article_id=number).order_by(Comment.create_time.asc()).all()
#     # todo relationship优化！！！
#     comments = collections.defaultdict(lambda: {"parent": None, "child": []})
#     for comment in comments_all:
#         if not (comment.parent_id or comment.root_id):
#             comments[comment.id]["parent"] = comment
#         else:
#             comments[comment.root_id]["child"].append(comment)
#
#     return render_template("blog_read.html", article=article, comments=comments.values(), comment_form=CommentForm(),
#                            reply_form=ReplyForm())


@blog_bp.route("/admin")
@login_required
def admin():
    categories = Category.get_own()
    articles = Article.get_own()
    return render_template("blog_admin.html", categories=categories, articles=articles)


# @blog_bp.route("/category")
# @login_required
# def category():
#     form_ = CategoryForm(user_email=current_user.email)
#     categories = Category.get_own()
#
#     return render_template("blog_category.html", categories=categories, form_=form_)


# @blog_bp.route("/category_del", methods=["POST"])
# @login_required
# @permission_decorator(Category)
# def category_del():
#     category_id = request.json.get("number")
#     cty = Category.query.get(category_id)
#     db.session.delete(cty)
#     db.session.commit()
#     flash(f"{cty.category} 删除成功！")
#     return jsonify({"success": True, "msg": "删除成功"})


# @blog_bp.route("/category_add", methods=["POST"])
# @login_required
# def category_add():
#     form_ = CategoryForm()
#     if form_.validate_on_submit():
#         new_cty = Category(category=form_.name.data, creator_id=current_user.id)
#         db.session.add(new_cty)
#         db.session.commit()
#         flash(f"{form_.data.get('name')}创建成功！")
#         return redirect(url_for("blog.category"))
#     if form_.errors:
#         flash('\n'.join(itertools.chain(*form_.errors.values())))
#     return redirect(url_for("blog.category"))


# @blog_bp.route("/article_add", methods=["GET", "POST"])
# @blog_bp.route("/article_edit/<int:number>", methods=["GET", "POST"])
# @permission_decorator(Article)
# @login_required
# def article_add(number=None):
#     article = Article.query.get(number) if number else Article()
#     form_ = ArticleForm()
#     if form_.validate_on_submit():
#         info = {
#             "title": form_.title.data,
#             "desc": form_.desc.data,
#             "body": form_.body.data,
#             "category_id": form_.category.data,
#             "creator_id": current_user.id
#         }
#         # update()方法是query的方法，刚初始化的模型类实例无法使用
#         # article.update(info)
#         update_attr(article, info)
#         if not number:
#             db.session.add(article)
#         db.session.commit()
#         flash(f"《{form_.title.data}》{'创建成功' if not number else '修改成功'}！")
#         return redirect(url_for("blog.admin"))
#     if form_.errors:
#         flash('\n'.join(itertools.chain(*form_.errors.values())))
#     # 如果获取修改页面，填充form表单数据
#     if request.method == "GET" and number:
#         form_.process(data={
#             "title": article.title,
#             "desc": article.desc,
#             "body": article.body,
#             "category": article.category_id,
#             "number": article.id
#         })
#
#     return render_template("blog_add.html", form_=form_, article=article)

#
# @blog_bp.route("/article_del", methods=["POST"])
# @login_required
# @login_user_permission_decorator(Article)
# def article_del():
#     article = Article.query.get(request.json.get("number"))
#     db.session.delete(article)
#     db.session.commit()
#     flash(f"文章《{article.title}》删除成功！")
#     return jsonify({"success": True, "msg": f"文章《{article.title}》删除成功！"})


# todo 类视图改造！！！！！
@blog_bp.route("/comment_add", methods=["POST"])
@login_required
def comment_add():
    def _deal_reply():
        info.update({
            "parent_id": form_.parent_comment_id.data,
            "root_id": form_.root_comment_id.data
        })

    def _deal_comment():
        info.update({})

    flag = request.form.get("parent_comment_id") is None
    form_ = CommentForm() if flag else ReplyForm()
    if form_.validate_on_submit():
        info = {
            "article_id": form_.article_id.data,
            "author_id": current_user.id,
            "body": form_.body.data
        }
        # todo 冻结 简化传参
        _deal_comment() if flag else _deal_reply()

        db.session.add(Comment(**info))
        db.session.commit()
        flash("评论成功！" if flag else "回复成功！")
    if form_.errors:
        flash('\n'.join(itertools.chain(*form_.errors.values())))
    return redirect(url_for("blog.read", number=form_.article_id.data))
