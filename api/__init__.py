from django.apps import AppConfig as BaseAppConfig
from django.utils.module_loading import autodiscover_modules


class AppConfig(BaseAppConfig):
    name = 'api'

    def ready(self):
        # Automatically import all receivers files
        autodiscover_modules('receivers')


default_app_config = 'api.AppConfig'
