render_kws = {
    "UserBaseForm_email": {
        "class": "form-control",
        "placeholder": "Email Address"
    },

    "UserBaseForm_password": {
        "class": "form-control",
        "placeholder": "Password"
    },

    "RegisterForm_email": {
        "class": "form-control",
        "placeholder": "Email Address"
    },

    "RegisterForm_username": {
        "class": "form-control",
        "placeholder": "Name"
    },

    "RegisterForm_password": {
        "class": "form-control",
        "placeholder": "Password"
    },

    "RegisterForm_confirm_password": {
        "class": "form-control",
        "placeholder": "ConfirmPassword"
    },

    "RegisterForm_age": {
        "class": "form-control"
    },

    "RegisterForm_gender": {
        "class": "form-control"
    },
    "RegisterForm_submit": {
        "class": "btn btn-lg btn-primary btn-block mt-2",
        "value": "注册"
    },
    "LoginForm_submit": {
        "class": "btn btn-lg btn-primary btn-block"
    },
    "LoginForm_remember": {
        "value": "Remember Me"
    },
    "CategoryForm_name": {
        "class": "form-control"
    },
    "CategoryForm_user_email": {
        "class": "form-control",
        "readonly": "readonly"
    },
    "CategoryForm_submit": {
        "class": "btn btn-primary",
        "value": " 新 增 ",
        # 指定Form标签的id，使Form标签外的button绑定form
        "form": "add_category_form"
    },
    "ArticleForm_all": {
        "class": "form-control"
    }
}


def get_kws(cls, column=None):
    return render_kws.get(f"{cls}_{column}") if column else render_kws.get(cls)
