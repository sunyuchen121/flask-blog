from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, BooleanField, TextAreaField, PasswordField, EmailField, \
    SelectField, HiddenField
from wtforms.validators import DataRequired, Length, equal_to, Email, NumberRange, ValidationError
from flask_ckeditor import CKEditorField
from templates.render_kws import get_kws
from flask_login import current_user
from models import Admin, Category

class UserBaseForm(FlaskForm):
    """ 用户相关, 基础表单模板 """
    email = EmailField("email", validators=[Email()], render_kw=get_kws(__qualname__, "email"))
    password = PasswordField("password", validators=[DataRequired(), Length(10, 50)],
                             render_kw=get_kws(__qualname__, "password"))


class RegisterForm(UserBaseForm):
    """注册表单"""
    username = StringField("username", validators=[DataRequired(), Length(1, 20)],
                           render_kw=get_kws(__qualname__, "username"))
    confirm_password = PasswordField("confirm_password", validators=[equal_to("password")],
                                     render_kw=get_kws(__qualname__, "confirm_password"))
    age = IntegerField("age", validators=[DataRequired(), NumberRange(1, 199)],
                       render_kw=get_kws(__qualname__, "age"))
    gender = SelectField("gender", validators=[DataRequired()], choices=list(zip((1, 2, 3), ("男", "女", "未知"))),
                         default=3, render_kw=get_kws(__qualname__, "gender"))
    op = HiddenField("op", validators=[DataRequired()])
    submit = SubmitField("submit", render_kw=get_kws(__qualname__, "submit"))

    def validate_email(self, field):
        exist_user = Admin.query.filter_by(email=field.data).first()
        if exist_user:
            raise ValidationError(f'{field.data}已被注册！')


class LoginForm(UserBaseForm):
    """登陆表单"""
    remember = BooleanField("remember")
    op = HiddenField("op", validators=[DataRequired()])
    submit = SubmitField("登 录", render_kw=get_kws(__qualname__, "submit"))

    def validate_email(self, field):
        exist_user = Admin.query.filter(Admin.email == field.data).first()
        if not exist_user:
            raise ValidationError(f"邮箱：{field.data}未注册！")
        if not exist_user.validate_password(self.password.data):
            raise ValidationError("密码错误！")


class ProfileForm(UserBaseForm):
    """个人资料修改表单"""
    site_title = StringField("site_title", validators=[Length(0, 20)])
    site_subtitle = StringField("site_subtitle", validators=[Length(0, 20)])
    about = TextAreaField("about", validators=[Length(0, 500)])


class CategoryForm(FlaskForm):
    name = StringField("分类名称", validators=[Length(1, 10), DataRequired()], render_kw=get_kws(__qualname__, "name"))
    user_email = StringField("创建人邮箱", validators=[DataRequired(), Email()],
                             render_kw=get_kws(__qualname__, "user_email"))
    op = HiddenField(validators=[DataRequired()])
    submit = SubmitField("submit", render_kw=get_kws(__qualname__, "submit"))

    def validate_user_email(self, field):
        # 防止前端修改create_user
        if field.data != current_user.email:
            raise ValidationError("创建人不可修改！")

    def validate_name(self, field):
        if Category.query.filter_by(category=field.data).first():
            raise ValidationError(f"分类-{field.data}也被创建！")


class ArticleForm(FlaskForm):
    """新增、修改文章表单"""
    title = StringField("标题:", validators=[Length(1, 25), DataRequired()], render_kw=get_kws(__qualname__, "all"))
    desc = StringField("文章简介:", validators=[Length(1, 100), DataRequired()], render_kw=get_kws(__qualname__, "all"))
    body = CKEditorField("文章主体:", validators=[DataRequired()])
    category = SelectField("所属分类:", validators=[DataRequired()], choices=[(18, "python")])
    number = HiddenField()
    op = HiddenField(validators=[DataRequired()])
    submit = SubmitField("创建", render_kw=get_kws("LoginForm_submit"))

    # def enabled_categories():
    #     return Category.query.filter_by(enabled=True)
    # category = QuerySelectField(query_factory=enabled_categories, allow_blank=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(cty.id, cty.category) for cty in
                                 Category.query.order_by(Category.create_time.asc()).all()]


class CommentForm(FlaskForm):
    """发表评论表单"""
    article_id = IntegerField("文章id", validators=[DataRequired()])
    body = TextAreaField("回复内容", validators=[DataRequired(), Length(1, 200)], render_kw=get_kws("ArticleForm_all"))
    submit = SubmitField("提 交")


class ReplyForm(CommentForm):
    """回复评论表单"""
    parent_user_email = EmailField("被回复人", validators=[DataRequired(), Email()],
                                   render_kw=get_kws("CategoryForm_user_email"))
    parent_comment = TextAreaField("被回复评论", validators=[DataRequired(), Length(1, 200)],
                                   render_kw=get_kws("CategoryForm_user_email"))
    parent_comment_id = IntegerField("父级评论id", validators=[DataRequired()])
    root_comment_id = IntegerField("根节点评论id", validators=[DataRequired()])
    # reply_submit = SubmitField("提 交", render_kw=get_kws("ReplyForm_submit"))
