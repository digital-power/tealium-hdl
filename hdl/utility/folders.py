import os
from datetime import datetime
from shutil import rmtree

def folder_filter(folder_path):
    """Filter to exclude common folders"""
    folder_list = folder_path.split('\\')
    last_part = folder_list[-1]

    return last_part not in ('.venv', '.vscode', '.ipynb_checkpoints', '.git', '__pycache__')


def scan_folders(folder_path):
    """Scans for all folders in a folder Recursively"""
    subitems = os.scandir(folder_path)
    subfolders = []
    for item in subitems:
        if item.is_dir() and folder_filter(item.name):
            found_folder_path = os.path.join(folder_path, item.name)
            subfolders.append(found_folder_path)
            subfolders += scan_folders(found_folder_path)

    return subfolders


def create_folder(folder_path):
    """Create folder. Delete possible existing folder"""
    if os.path.exists(folder_path):
        rmtree(folder_path)

    os.mkdir(folder_path)

def generate_folder_name(folder_name):
    """Generate folder name from a date & given folder name"""
    return datetime.today().strftime('%Y-%m-%d') + folder_name
