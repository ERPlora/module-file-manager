from django.urls import path
from . import views

app_name = 'file_manager'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('files/', views.files, name='files'),
    path('settings/', views.settings, name='settings'),
]
