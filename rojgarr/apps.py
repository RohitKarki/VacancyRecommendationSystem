from django.apps import AppConfig


class RojgarrConfig(AppConfig):
    name = 'rojgarr'

    def ready(self):
       from .cron import start
       start()