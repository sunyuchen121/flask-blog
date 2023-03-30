from celery import Celery


def make_up_celery(name):
    _c = Celery(name)
    _c.config_from_object("conf.CeleryConf")
    return _c
