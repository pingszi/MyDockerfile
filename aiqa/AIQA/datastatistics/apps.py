import logging

from django.apps import AppConfig


class DatastatisticsConfig(AppConfig):
    name = 'datastatistics'

    # **app名称
    verbose_name = "数据统计"

logger = logging.getLogger("datastatistics")