import collections

from flask import g, request, session, current_app, jsonify, redirect, url_for, views, abort, flash
from extends import login_mgr, db
from models import Admin, Article
from urllib.parse import urlparse, urljoin
import numbers
import itertools


def login_required(func):
    def inner():
        resp = {
            "success": False,
            "msg": "请先登录，该页面需要登陆后才可访问！"
        }
        return jsonify(resp)

    if not session.get("is_login", False):
        return inner

    return func


@login_mgr.user_loader
def get_user(user_id):
    user_info = Admin.query.get(int(user_id))
    return user_info


def update_attr(obj, data_dict):
    for _k, _v in data_dict.items():
        setattr(obj, _k, _v)
    return obj


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def redirect_back(default_url="index", **kwargs):
    target = request.args.get("next")
    if target and is_safe_url(target):
        return redirect(target)
    return redirect(url_for(default_url))


class PageController:

    def __init__(self, paginate, show_pages: int = 5, **kwargs):
        self.paginate = paginate
        self.show_pages = show_pages if show_pages >= 5 else 5
        self.default_cls = kwargs.get("_cls", "page-item")

    @property
    def is_first(self):
        """是否第一页"""
        return not self.paginate.has_prev

    @property
    def is_last(self):
        """是否最后一页"""
        return not self.paginate.has_next

    @property
    def last_page(self):
        """最后一页的页码, 也是总页数"""
        return self.paginate.pages

    def __iter__(self):
        return self.paginate.__iter__()

    def generate_ctl(self):
        pass

    def get_show_pages(self):
        """
        1. 如果展示页数大于等于总页数, 直接返回所有页数
        2. 如果展示页数小于总页数, 返回已当前页数为中心的前后各一半页数. 如果前/后的页数不足一半, 就把页数加到另一半
        :return:
        """
        if self.show_pages >= self.paginate.pages:
            return list(range(1, self.paginate.pages + 1))
        page_begin = max(self.paginate.page - self.show_pages // 2, 1)
        page_end = page_begin + self.show_pages - 1
        if page_end > self.paginate.pages:
            page_begin = page_end - self.show_pages
        return list(range(page_begin, page_end + 1))

    def show_index(self):
        """
        1. 当前页 active
        4. 前/后两方, 有一方超过两页, 前/后添加 disabled ...
        :return:
        """
        li_obj = collections.namedtuple("li_obj", "index cls current")
        result = []

        pages = self.get_show_pages()
        for page in pages:
            # 是否为当前页
            if page == self.paginate.page:
                item = self.default_cls + " active"
                current = True
            else:
                item = self.default_cls
                current = False
            li_item = li_obj(page, item, current)
            result.append(li_item)
        if pages:
            li_item = li_obj("...", self.default_cls + " disabled", None)
            if pages[0] != 1:
                result.insert(0, li_item)
            if pages[-1] != self.paginate.pages:
                result.append(li_item)
        return result


def register_views(app, cls, url, endpoint, param, param_type="str"):
    if param:
        url = f"{url}<{param}:{param_type}>"
    app.add_url_rule(url, cls.as_view(endpoint))



