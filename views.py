"""
File Manager Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('file_manager', 'dashboard')
@htmx_view('file_manager/pages/dashboard.html', 'file_manager/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('file_manager', 'files')
@htmx_view('file_manager/pages/files.html', 'file_manager/partials/files_content.html')
def files(request):
    """Files view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('file_manager', 'settings')
@htmx_view('file_manager/pages/settings.html', 'file_manager/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

