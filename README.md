# File Manager Module

File storage, organization, and sharing.

## Features

- Upload and manage files with metadata (name, type, size, description)
- Organize files into a hierarchical folder structure (nested folders)
- Track file type and size for each stored file
- Browse and search files across folders
- Dashboard with overview of storage usage and recent files

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > File Manager > Settings**

## Usage

Access via: **Menu > File Manager**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/file_manager/dashboard/` | Overview of storage usage and recent file activity |
| Files | `/m/file_manager/files/` | Browse, upload, and manage files and folders |
| Settings | `/m/file_manager/settings/` | Configure file manager module settings |

## Models

| Model | Description |
|-------|-------------|
| `Folder` | Hierarchical folder structure with nested parent/child support |
| `File` | Stored file record with name, type, size, path, description, and folder assignment |

## Permissions

| Permission | Description |
|------------|-------------|
| `file_manager.view_file` | View files and folders |
| `file_manager.add_file` | Upload new files and create folders |
| `file_manager.change_file` | Edit file and folder details |
| `file_manager.delete_file` | Delete files and folders |
| `file_manager.manage_settings` | Manage file manager module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
