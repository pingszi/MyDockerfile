import logging

from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = 'common'

    # **app名称
    verbose_name = "基础数据管理"

logger = logging.getLogger("common")
