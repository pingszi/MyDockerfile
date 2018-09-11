import logging

from django.apps import AppConfig


class MgbaseConfig(AppConfig):
    name = 'mgbase'

    # **app名称
    verbose_name = "后台管理"

logger = logging.getLogger("mgbase")
