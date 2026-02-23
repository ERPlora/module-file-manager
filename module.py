    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'file_manager'
    MODULE_NAME = _('File Manager')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'folder-open-outline'
    MODULE_DESCRIPTION = _('File storage, organization and sharing')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'documents'

    MENU = {
        'label': _('File Manager'),
        'icon': 'folder-open-outline',
        'order': 72,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Files'), 'icon': 'folder-open-outline', 'id': 'files'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'file_manager.view_file',
'file_manager.add_file',
'file_manager.change_file',
'file_manager.delete_file',
'file_manager.manage_settings',
    ]
