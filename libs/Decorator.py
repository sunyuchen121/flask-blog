from flask import request, jsonify
from flask_login import current_user, login_required
import operator
import functools
from libs.Utils import get_actual_child_path


def permission_decorator(cls, func):
    @functools.wraps(func)
    def permission_deny_resp():
        return jsonify({"success": False, "msg": u"权限不足！"})

    @functools.wraps(func)
    def inner(*args, **kwargs):
        user_id, is_super, data_id = current_user.id, current_user._is_super, None
        if not is_super:
            if request.content_type and not request.content_type.startswith("application/json"):
                data_id = request.json.get("number")
            else:
                data_id = request.values.get("number")
            print(data_id)
            # 没有data_id可能是add请求, 交给具体的view自己判断data_id是否必填.
            if not data_id:
                return func(*args, **kwargs)
            data_role_id = getattr(cls.query.get(data_id), "creator_id")
            return func(*args, **kwargs) if data_role_id == user_id else permission_deny_resp()

        return func(*args, **kwargs)

    return inner


def login_user_permission_decorator(cls, ignore_urls=tuple()):
    def warp(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            child_path = get_actual_child_path()
            if ignore_urls and child_path in ignore_urls:
                print("**********" * 20)
                return func(*args, **kwargs)
            print("***********************************")
            return login_required(permission_decorator(cls, func))(*args, **kwargs)

        return inner

    return warp
