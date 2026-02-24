from django.contrib import admin

from .models import Folder, File

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['folder', 'name', 'file_type', 'size_bytes', 'file_path', 'created_at']
    search_fields = ['name', 'file_type', 'file_path', 'description']
    readonly_fields = ['created_at', 'updated_at']

