from django.urls import path
from . import views

app_name = 'file_manager'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('files/', views.folders_list, name='files'),


    # Folder
    path('folders/', views.folders_list, name='folders_list'),
    path('folders/add/', views.folder_add, name='folder_add'),
    path('folders/<uuid:pk>/edit/', views.folder_edit, name='folder_edit'),
    path('folders/<uuid:pk>/delete/', views.folder_delete, name='folder_delete'),
    path('folders/<uuid:pk>/toggle/', views.folder_toggle_status, name='folder_toggle_status'),
    path('folders/bulk/', views.folders_bulk_action, name='folders_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
