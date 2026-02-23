from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

class Folder(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'file_manager_folder'

    def __str__(self):
        return self.name


class File(HubBaseModel):
    folder = models.ForeignKey('Folder', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    file_type = models.CharField(max_length=50, blank=True, verbose_name=_('File Type'))
    size_bytes = models.PositiveIntegerField(default=0, verbose_name=_('Size Bytes'))
    file_path = models.CharField(max_length=500, verbose_name=_('File Path'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta(HubBaseModel.Meta):
        db_table = 'file_manager_file'

    def __str__(self):
        return self.name

