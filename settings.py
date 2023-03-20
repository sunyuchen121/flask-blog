import os


class CommonConf:
    aaa = os.environ.get("db.path")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/flask_blog?charset=utf8"
    SQLALCHEMY_ECHO = True
    SECRET_KEY = "asdhjkfnskjnd,smtnrme5#@$#@"
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_CODE_THEME = "monokai"
    CKEDITOR_HEIGHT = 800


class ContainerConf(CommonConf):
    pass
