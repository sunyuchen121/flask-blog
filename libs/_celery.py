from celery import Celery


def celery_factory(name):
    _c = Celery(name)
    _c.config_from_object("conf.CeleryConf")
    return _c
