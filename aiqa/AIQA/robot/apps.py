import logging

from django.apps import AppConfig


class RobotConfig(AppConfig):
    name = 'robot'

logger = logging.getLogger("robot")
