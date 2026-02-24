"""Tests for file_manager models."""
import pytest
from django.utils import timezone

from file_manager.models import Folder


@pytest.mark.django_db
class TestFolder:
    """Folder model tests."""

    def test_create(self, folder):
        """Test Folder creation."""
        assert folder.pk is not None
        assert folder.is_deleted is False

    def test_str(self, folder):
        """Test string representation."""
        assert str(folder) is not None
        assert len(str(folder)) > 0

    def test_soft_delete(self, folder):
        """Test soft delete."""
        pk = folder.pk
        folder.is_deleted = True
        folder.deleted_at = timezone.now()
        folder.save()
        assert not Folder.objects.filter(pk=pk).exists()
        assert Folder.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, folder):
        """Test default queryset excludes deleted."""
        folder.is_deleted = True
        folder.deleted_at = timezone.now()
        folder.save()
        assert Folder.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, folder):
        """Test toggling is_active."""
        original = folder.is_active
        folder.is_active = not original
        folder.save()
        folder.refresh_from_db()
        assert folder.is_active != original


