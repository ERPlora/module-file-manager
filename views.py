"""
File Manager Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import Folder, File

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('file_manager', 'dashboard')
@htmx_view('file_manager/pages/index.html', 'file_manager/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_folders': Folder.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# Folder
# ======================================================================

FOLDER_SORT_FIELDS = {
    'name': 'name',
    'parent': 'parent',
    'is_active': 'is_active',
    'created_at': 'created_at',
}

def _build_folders_context(hub_id, per_page=10):
    qs = Folder.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'folders': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_folders_list(request, hub_id, per_page=10):
    ctx = _build_folders_context(hub_id, per_page)
    return django_render(request, 'file_manager/partials/folders_list.html', ctx)

@login_required
@with_module_nav('file_manager', 'files')
@htmx_view('file_manager/pages/folders.html', 'file_manager/partials/folders_content.html')
def folders_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Folder.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query))

    order_by = FOLDER_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'parent', 'is_active']
        headers = ['Name', 'self', 'Is Active']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='folders.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='folders.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'file_manager/partials/folders_list.html', {
            'folders': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'folders': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def folder_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        obj = Folder(hub_id=hub_id)
        obj.name = name
        obj.is_active = is_active
        obj.save()
        return _render_folders_list(request, hub_id)
    return django_render(request, 'file_manager/partials/panel_folder_add.html', {})

@login_required
def folder_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Folder, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_folders_list(request, hub_id)
    return django_render(request, 'file_manager/partials/panel_folder_edit.html', {'obj': obj})

@login_required
@require_POST
def folder_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Folder, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_folders_list(request, hub_id)

@login_required
@require_POST
def folder_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Folder, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_folders_list(request, hub_id)

@login_required
@require_POST
def folders_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Folder.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_folders_list(request, hub_id)


@login_required
@permission_required('file_manager.manage_settings')
@with_module_nav('file_manager', 'settings')
@htmx_view('file_manager/pages/settings.html', 'file_manager/partials/settings_content.html')
def settings_view(request):
    return {}

