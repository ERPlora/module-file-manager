from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FileManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file_manager'
    label = 'file_manager'
    verbose_name = _('File Manager')

    def ready(self):
        pass
