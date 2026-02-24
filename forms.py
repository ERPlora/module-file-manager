from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Folder

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'parent': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

