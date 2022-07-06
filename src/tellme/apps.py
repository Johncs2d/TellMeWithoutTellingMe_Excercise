from django.apps import AppConfig
from src import container


class TellmeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tellme'

    def ready(self):
        container.wire(modules=[".views"])