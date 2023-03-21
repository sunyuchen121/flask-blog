import copy
import numbers
import itertools
from flask import views, request, abort, jsonify, flash
from extends import db
from libs.Utils import get_actual_child_path


class EntryMethodViewBase(views.MethodView):
    pass


class EntryView(views.MethodView):
    # decorators = [login_required]
    ALLOW_OP: tuple = ("create", "edit", "delete")
    ALLOW_PATH = ("test1", "test2")
    GET_DEFAULT_FUNC: str = ""
    POST_DEFAULT_FUNC: str = ""
    MODEL: object = ""
    FORM: object = ""
    DEL_SHOW_KEY: str = ""

    def __init__(self):
        self.form_ = self.form()
        if request.method == "POST":
            # request.values == request.form + request.args
            self.data = request.form or request.json
            # 如果浏览器传过来的是json格式的字符串数据，但是请求头中又没有指定content-type ：application/json，如果你直接调用request.json 会直接报错，返回401错误
            # self.json_data = request.json

        super(EntryView, self).__init__()

    # def get(self, number):
    #     if not number or not isinstance(number, numbers.Integral):
    #         abort(404)
    #     return self.json_resp(data=self.get_data(number))

    def get(self, *args, **kwargs):
        child_path = get_actual_child_path()
        # if self.__class__.NUMBER_MUST and not isinstance(number, numbers.Integral):
        #     flag = True

        process_view = getattr(self, f"{child_path}_process", None)
        if not callable(process_view) and self.__class__.GET_DEFAULT_FUNC:
            process_view = getattr(self, self.__class__.GET_DEFAULT_FUNC, None)
        if not callable(process_view):
            abort(404)
        return process_view(*args, **kwargs)

    def post(self):
        """
        create: id_为空，数据从request.form中获取
        edit: id_不为空，数据也从request.form获取
        delete: id_为空，具体id_从request.json中获取
        """
        op = self.data.get("op")
        process_view = getattr(self, f"{op}_data", None)
        if not process_view and self.__class__.POST_DEFAULT_FUNC:
            process_view = getattr(self, self.__class__.POST_DEFAULT_FUNC, None)
        if not process_view or not callable(process_view):
            abort(404)
        return process_view()

    def create_data(self):
        """
        op: create
        """
        if self.form_.validate_on_submit():
            self.create(self.data)
            return self.json_resp(msg="新增成功！")
        self.flash_form_error()
        return self.json_resp(False, "新增数据失败！")

    def edit_data(self):
        """
        op: edit
        """
        if self.form_.validate_on_submit():
            data = copy.deepcopy(self.data)
            id_ = data.pop("number", None)

            info = self.update(id_, data)
            if info is not False:
                return self.json_resp(msg="修改数据成功！")
        self.flash_form_error()
        return self.json_resp(False, "修改数据失败！")

    def delete_data(self, show_key=None):
        """
        op: delete
        """
        id_ = self.data.get("number", int)
        data = self.delete(id_)
        if not data:
            return self.json_resp(False, "删除失败！")
        show_key = show_key or self.__class__.DEL_SHOW_KEY
        msg = f"{getattr(data, show_key, '') if show_key else ''}删除成功！"
        flash(msg)
        return self.json_resp(msg=msg)

    @staticmethod
    def json_resp(flag: True | False = True, msg: str = "", data=None):
        return jsonify({
            "success": flag,
            "msg": msg,
            "data": data
        })

    def flash_form_error(self):
        if self.form_.errors:
            flash("".join(itertools.chain(*self.form_.errors.values())))

    @property
    def query(self):
        return self.model.query

    def get_data(self, id_: int):
        return self.query.get(id_)

    def filter_dict(self, **filters: dict):
        return self.query.filter_by(**filters)

    @property
    def form(self):
        return self.__class__.FORM

    @property
    def model(self):
        return self.__class__.MODEL

    def create(self, info):
        data = self.make_up(info)
        db.session.add(data)
        db.session.commit()
        return data

    def update(self, _id: int, info: dict):
        query_obj = self.query.filter_by(id=_id)
        affect_rows = query_obj.update(info)
        if affect_rows == 1:
            db.session.commit()
            return query_obj.first()
        else:
            db.session.rollback()
            return False

    def delete(self, id_):
        data = self.get_data(id_)
        if not data:
            return False
        db.session.delete(data)
        db.session.commit()
        return data

    def make_up(self, info, model=None):
        if not model:
            model = self.model
        return model(**info)
