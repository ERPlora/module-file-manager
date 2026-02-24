"""Tests for file_manager views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('file_manager:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('file_manager:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('file_manager:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestFolderViews:
    """Folder view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('file_manager:folders_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('file_manager:folders_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('file_manager:folders_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('file_manager:folders_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('file_manager:folders_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('file_manager:folders_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('file_manager:folder_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('file_manager:folder_add')
        data = {
            'name': 'New Name',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, folder):
        """Test edit form loads."""
        url = reverse('file_manager:folder_edit', args=[folder.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, folder):
        """Test editing via POST."""
        url = reverse('file_manager:folder_edit', args=[folder.pk])
        data = {
            'name': 'Updated Name',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, folder):
        """Test soft delete via POST."""
        url = reverse('file_manager:folder_delete', args=[folder.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        folder.refresh_from_db()
        assert folder.is_deleted is True

    def test_toggle_status(self, auth_client, folder):
        """Test toggle active status."""
        url = reverse('file_manager:folder_toggle_status', args=[folder.pk])
        original = folder.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        folder.refresh_from_db()
        assert folder.is_active != original

    def test_bulk_delete(self, auth_client, folder):
        """Test bulk delete."""
        url = reverse('file_manager:folders_bulk_action')
        response = auth_client.post(url, {'ids': str(folder.pk), 'action': 'delete'})
        assert response.status_code == 200
        folder.refresh_from_db()
        assert folder.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('file_manager:folders_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('file_manager:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('file_manager:settings')
        response = client.get(url)
        assert response.status_code == 302

